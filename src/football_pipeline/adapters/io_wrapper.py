import json
import urllib.request
from enum import Enum, auto
from pathlib import Path
from typing import Protocol, runtime_checkable

import attrs
import polars as pl
import yaml


class FileType(Enum):
    YAML = auto()
    FOOTBALL_API = auto()
    JSON = auto()
    PARQUET = auto()


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
                return yaml.safe_load(Path(path).read_text(), **kwargs)
            case FileType.FOOTBALL_API:
                headers = {"User-Agent": "Mozilla/5.0"}
                request = urllib.request.Request(path, headers=headers, **kwargs)
                with urllib.request.urlopen(request) as url:
                    return json.load(url)
            case FileType.PARQUET:
                return pl.scan_parquet(path, **kwargs)
            case _:
                raise ValueError(f"Given invalid file type {file_type} for path {path}")

    def write(self, path: str, data, file_type: FileType, **kwargs) -> bool:
        save_path = Path(path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        match file_type:
            case FileType.YAML:
                save_path.write_text(yaml.safe_dump(data, **kwargs))
                return True
            case FileType.JSON:
                save_path.write_text(json.dumps(data, **kwargs))
                return True
            case FileType.PARQUET:
                data.write_parquet(path, **kwargs)
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
        return self.db[path]

    def write(self, path: str, data, file_type: FileType, **kwargs) -> bool:
        self.log.append(
            {"func": "write", "path": path, "file_type": file_type, "kwargs": kwargs}
        )
        self.db[path] = data
