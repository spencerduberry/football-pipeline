import argparse  # parses command-line args
import os
import uuid
from datetime import datetime

from football_pipeline.io import extract_data, read_yaml, write_to_parquet
from football_pipeline.logger import log_func, logger
from football_pipeline.transform import add_ingestion_columns


@log_func
def run_raw_layer(config_path: str) -> dict:
    config = read_yaml(config_path)

    if not config:
        return {"valid_config": False}

    save_path = config.get("save_root", "./")
    batch_guid = str(uuid.uuid4())
    date_time = datetime.now()
    date_time_str = date_time.strftime("%y%m%d_%H%M%S")
    successes = {}

    for k, v in config.get("endpoints", {}).items():
        path = v.get("path", "")
        keys = v.get("keys", [])
        res = extract_data(path, keys)

        if isinstance(res, list):
            logger.error("Error: retrieved onbject was a list.")
            raise ValueError(res)

        res = {
            k: add_ingestion_columns(v, batch_guid, date_time) for k, v in res.items()
        }

        for k, v in res.items():
            file_save_path = f"{save_path}/{k}/{date_time_str}.parquet"
            os.makedirs(os.path.dirname(file_save_path), exist_ok=True)
            successes[file_save_path] = write_to_parquet(v, file_save_path)

    return successes


# argparse reads the config path to the YAML and runs raw layer
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse config path")
    parser.add_argument(
        "--config-path", type=str, help="Path to the configuration file"
    )
    args = parser.parse_args()

    print(run_raw_layer(args.config_path))
