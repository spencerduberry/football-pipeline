import argparse  # parses command-line args

from football_pipeline.adapters.fs_wrapper import FSLocal
from football_pipeline.adapters.io_wrapper import FileType, IOWrapper
from football_pipeline.adapters.logger import RealLogger
from football_pipeline.adapters.repo import Repo
from football_pipeline.adapters.time import new_guid, time_now


def run_raw_layer(config_path: str, repo: Repo) -> dict[str, bool]:
    config = repo.io.read(config_path, FileType.YAML)
    repo.logger.info(msg="successfully read yaml.", config_path=config_path)
    if not config:
        return {"valid_config": False}

    save_path = config.get("save_root", "./")
    date_time_str = repo.time_func()
    successes = {}

    for k, v in config.get("endpoints", {}).items():
        path = v.get("path", "")
        keys = v.get("keys", [])
        repo.logger.info(msg="attempting to read", path=path, keys=keys)
        api_response = repo.io.read(path, FileType.FOOTBALL_API)
        repo.logger.info(msg="successfully received message.", path=path, keys=keys)

        file_save_path = f"{save_path}/{k}/{date_time_str}.json"
        successes[file_save_path] = repo.io.write(
            file_save_path, api_response, FileType.JSON
        )

    return successes


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
    print(run_raw_layer(args.config_path, repo))
