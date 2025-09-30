import json
import urllib.request
from enum import Enum, auto
from typing import Protocol, runtime_checkable

import attrs
import pandas as pd
import yaml


# enum = a restrictive, immutable set of options
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
        if file_type not in self.db:
            self.db[file_type] = {}
        self.db[file_type][path] = data


"""from enum import Enum, auto
from typing import Protocol, runtime_checkable

import attrs


# enum = a restrictive, immutable set of options
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
    read_funcs: dict
    write_funcs: dict

    def setup(self) -> bool:
        return True

    def teardown(self) -> bool:
        return True

    def read(self, path: str, file_type: FileType, **kwargs):
        if file_type in self.read_funcs:
            read_func = self.read_funcs[file_type]
            return read_func(path, **kwargs)
        raise ValueError(f"Given invalid file type {file_type} for path {path}")

    def write(self, path: str, data, file_type: FileType, **kwargs) -> bool:
        if file_type in self.write_funcs:
            write_func = self.write_funcs[file_type]
            return write_func(path, data, **kwargs)
        raise ValueError(f"Given invalid file type {file_type} for path {path}")


def read_yaml(path, **kwargs):
    with open(path, "r") as file:
        return yaml.safe_load(file, **kwargs)


def read_parquet(path, **kwargs):
    return pd.read_parquet(path, **kwargs)


def read_football_api(path, **kwargs):
    headers = {"User-Agent": "Mozilla/5.0"}
    request = urllib.request.Request(path, headers=headers, **kwargs)
    with urllib.request.urlopen(request) as url:
        return json.load(url)


def write_yaml(path, data, **kwargs):
    with open(path, "w") as file:
        yaml.safe_dump(data, file, **kwargs)
    return True


def write_parquet(path, data, **kwargs):
    data.to_parquet(path, **kwargs)
    return True


read_funcs = {
    FileType.YAML: read_yaml,
    FileType.PARQUET: read_parquet,
    FileType.FOOTBALL_API: read_football_api,
}

write_funcs = {
    FileType.YAML: write_yaml,
    FileType.PARQUET: write_parquet,
}

io = IOWrapper(read_funcs, write_funcs)

from enum import Enum, auto
from typing import Protocol, runtime_checkable

import attrs


# enum = a restrictive, immutable set of options
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
    io_classes: dict

    def setup(self) -> bool:
        return True

    def teardown(self) -> bool:
        return True

    def read(self, path: str, file_type: FileType, **kwargs):
        if file_type in self.io_classes:
            io_class = self.io_classes[file_type]
            return io_class.read(path, **kwargs)
        raise ValueError(f"Given invalid file type {file_type} for path {path}")

    def write(self, path: str, data, file_type: FileType, **kwargs) -> bool:
        if file_type in self.io_classes:
            io_class = self.io_classes[file_type]
            if hasattr(io_class, "write"):
                return io_class.write(path, data, **kwargs)
        raise ValueError(f"Given invalid file type {file_type} for path {path}")


class YamlIo:
    def read(path, **kwargs):
        with open(path, "r") as file:
            return yaml.safe_load(file, **kwargs)

    def write(path, data, **kwargs):
        with open(path, "w") as file:
            yaml.safe_dump(data, file, **kwargs)
        return True


class ParquetIo:
    def read(path, **kwargs):
        return pd.read_parquet(path, **kwargs)

    def write(path, data, **kwargs):
        data.to_parquet(path, **kwargs)
        return True


class FootballApi:
    def read(path, **kwargs):
        headers = {"User-Agent": "Mozilla/5.0"}
        request = urllib.request.Request(path, headers=headers, **kwargs)
        with urllib.request.urlopen(request) as url:
            return json.load(url)

    def write(path, data, **kwargs):
        raise NotImplementedError


io_classes = {
    FileType.YAML: YamlIo(),
    FileType.PARQUET: ParquetIo(),
    FileType.FOOTBALL_API: FootballApi(),
}

io = IOWrapper(io_classes)"""
