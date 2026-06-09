import argparse  # parses command-line args

import polars as pl

from football_pipeline.adapters.fs_wrapper import FSLocal
from football_pipeline.adapters.io_wrapper import FileType, IOWrapper
from football_pipeline.adapters.logger import RealLogger
from football_pipeline.adapters.repo import Repo
from football_pipeline.adapters.time import new_guid, time_now


def run_raw_player_layer(config_path: str, repo: Repo) -> dict[str, bool]:
    config = repo.io.read(config_path, FileType.YAML)
    if not config:
        return {"valid_config": False}

    dfs, fails = get_api_responses(
        repo,
        config.get("min_player_id", 0),
        config.get("max_player_id", 999),
        config["endpoint"],
    )
    if not dfs:
        raise_if_failed(fails)
    save_path = config.get("save_root", "./")
    date_time_str = repo.time_func().strftime("%Y%m%d_%H%M%S")
    save_data(
        repo,
        f"{save_path}/history",
        date_time_str,
        [pl.DataFrame(df["history"]) for df in dfs],
    )
    save_data(
        repo,
        f"{save_path}/history_past",
        date_time_str,
        [pl.DataFrame(df["history_past"]) for df in dfs],
    )
    raise_if_failed(fails)
    return True


def get_api_responses(
    repo: Repo, min_player_id: int, max_player_id: int, path: str
) -> tuple[list[dict], list[tuple[str, Exception]]]:
    dfs = []
    fails = []

    for player_id in range(min_player_id, max_player_id):
        player_endpoint = f"{path}/{player_id}"
        try:
            api_response = repo.io.read(player_endpoint, FileType.FOOTBALL_API)
            dfs.append(api_response)
        except Exception as e:
            fails.append((player_endpoint, e))
    return dfs, fails


def save_data(repo, save_path, date_time_str, dfs):
    all_players = pl.concat(dfs)
    file_save_path = f"{save_path}/{date_time_str}.parquet"
    repo.io.write(file_save_path, all_players, FileType.PARQUET)


def raise_if_failed(fails: list[tuple[str, Exception]]) -> None:
    if fails:
        failed_endpoints = "\n".join([f[0] for f in fails])
        errors = "\n".join([str(f[1]) for f in fails])
        raise RuntimeError(f"{failed_endpoints = }{errors = }")


# argparse reads the config path to the YAML and runs raw layer
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse config path")
    parser.add_argument(
        "--config-path", type=str, help="Path to the configuration file"
    )
    args = parser.parse_args()
    repo = Repo(
        io=IOWrapper(),
        fs=FSLocal(),
        logger=RealLogger(__file__),
        time_func=time_now,
        guid_func=new_guid,
    )
    print(run_raw_player_layer(args.config_path, repo))
