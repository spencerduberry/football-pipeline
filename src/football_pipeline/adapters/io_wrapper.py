import json
import urllib.request
from enum import Enum, auto
from typing import Protocol, runtime_checkable

import attrs
import pandas as pd
import yaml


class FileType(Enum):
    PARQUET = auto()
    YAML = auto()
    FOOTBALL_API = auto()


@runtime_checkable
class IOProtocol(Protocol):
    def setup(self) -> bool: ...

    def teardown(self) -> bool: ...

    def read(self, path: str, file_type: FileType, **kwargs): ...

    def write(self, path: str, data, file_type: FileType, **kwargs) -> bool: ...


@attrs.define
class IOWrapper:
    def setup(self) -> bool:
        return True

    def teardown(self) -> bool:
        return True

    def read(self, path: str, file_type: FileType, **kwargs):
        match file_type:
            case FileType.YAML:
                with open(path, "r") as file:
                    return yaml.safe_load(file, **kwargs)
            case FileType.PARQUET:
                return pd.read_parquet(path, **kwargs)
            case FileType.FOOTBALL_API:
                headers = {"User-Agent": "Mozilla/5.0"}
                request = urllib.request.Request(path, headers=headers, **kwargs)
                with urllib.request.urlopen(request) as url:
                    return json.load(url)
            case _:
                raise ValueError(f"Given invalid file type {file_type} for path {path}")

    def write(self, path: str, data, file_type: FileType, **kwargs) -> bool:
        match file_type:
            case FileType.YAML:
                with open(path, "w") as file:
                    yaml.safe_dump(data, file, **kwargs)
                return True
            case FileType.PARQUET:
                data.to_parquet(path, **kwargs)
                return True
            case _:
                raise ValueError(f"Given invalid file type {file_type} for path {path}")


@attrs.define
class FakeIOWrapper:
    db: dict = attrs.field(default=attrs.Factory(dict))
    log: list = attrs.field(default=attrs.Factory(list))

    def setup(self) -> bool:
        return True

    def teardown(self) -> bool:
        return True

    def read(self, path: str, file_type: FileType, **kwargs):
        self.log.append(
            {"func": "read", "path": path, "file_type": file_type, "kwargs": kwargs}
        )
        return self.db[file_type][path]

    def write(self, path: str, data, file_type: FileType, **kwargs) -> bool:
        self.log.append(
            {"func": "write", "path": path, "file_type": file_type, "kwargs": kwargs}
        )
        self.db[file_type][path] = data
