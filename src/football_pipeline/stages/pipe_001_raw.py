import argparse  # parses command-line args
import os

from football_pipeline.adapters.fs_wrapper import FSLocal
from football_pipeline.adapters.io_wrapper import FileType, IOWrapper
from football_pipeline.adapters.logger import RealLogger
from football_pipeline.adapters.repo import Repo
from football_pipeline.adapters.time import new_guid, time_now
from football_pipeline.domain.transform import add_ingestion_columns, convert_data_to_df


def run_raw_layer(config_path: str, repo: Repo) -> dict:
    config = repo.io.read(config_path, FileType.YAML)

    if not config:
        return {"valid_config": False}

    save_path = config.get("save_root", "./")
    batch_guid = repo.guid_func()
    date_time_str = repo.time_func()
    successes = {}

    for k, v in config.get("endpoints", {}).items():
        path = v.get("path", "")
        keys = v.get("keys", [])
        api_response = repo.io.read(path, FileType.FOOTBALL_API)
        res = convert_data_to_df(api_response, path, keys)

        if isinstance(res, list):
            repo.logger.error({"df": res, "err": "Retrieved object was a list."})
            raise ValueError(res)

        res = {
            k: add_ingestion_columns(v, batch_guid, date_time_str)
            for k, v in res.items()
        }

        for k, v in res.items():
            file_save_path = f"{save_path}/{k}/{date_time_str}.parquet"
            repo.fs.create_dir(os.path.dirname(file_save_path))
            successes[file_save_path] = repo.io.write(
                file_save_path, v, FileType.PARQUET
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
