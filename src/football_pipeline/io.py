import os
import yaml


def read_yaml(path: str) -> dict:
    """
    Loads a YAML file from the given path and returns its contents as a dict.

    Args:
        path: the path to the YAML file.

    Returns:
        A dict representation of the YAML file or an empty dict on error.
    """
    try:
        abs_path = os.path.abspath(path)

        with open(path, "r") as file:
            data = yaml.safe_load(file)

        if data is None:
            print(
                f"Warning: {abs_path} is empty or invalid YAML. Returning empty dict."
            )
            return {}

        return data

    except (yaml.YAMLError, Exception) as e:
        print(f"Error loading YAML from {path}: {e}")
        return {}
