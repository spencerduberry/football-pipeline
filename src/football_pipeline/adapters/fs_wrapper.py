import glob
import os
import shutil
from copy import deepcopy
from typing import Protocol, runtime_checkable

import attrs


@runtime_checkable
class FSProtocol(Protocol):
    def create_dir(self, path: str) -> bool: ...

    def move(self, old_path: str, new_path: str) -> bool: ...

    def copy(self, old_path: str, new_path: str) -> bool: ...

    def delete(self, path: str) -> bool: ...

    def list_files(self, path: str, recursive: bool = False) -> list[str]: ...


@attrs.define
class FSLocal:
    def create_dir(self, path: str) -> bool:
        os.makedirs(path, exist_ok=True)
        return True

    def move(self, old_path: str, new_path: str) -> bool:
        os.rename(old_path, new_path)
        return True

    def copy(self, old_path: str, new_path: str) -> bool:
        shutil.copyfile(old_path, new_path)
        return True

    def delete(self, path: str) -> bool:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        else:
            return False
        return True

    def list_files(self, path: str, recursive: bool = False) -> list[str]:
        return glob.glob(path, recursive=recursive)


@attrs.define
class FakeFSLocal:
    db: dict = attrs.field(default=attrs.Factory(dict))
    log: list = attrs.field(default=attrs.Factory(list))

    def create_dir(self, path: str) -> bool:
        self.log.append({"func": "create_dir", "path": path})
        self.db[path] = {}
        return True

    def move(self, old_path: str, new_path: str) -> bool:
        self.log.append({"func": "move", "old_path": old_path, "new_path": new_path})
        self.db[new_path] = self.db.pop(old_path)
        return True

    def copy(self, old_path: str, new_path: str) -> bool:
        self.log.append({"func": "copy", "old_path": old_path, "new_path": new_path})
        self.db[new_path] = deepcopy(self.db[old_path])
        return True

    def delete(self, path: str) -> bool:
        self.log.append({"func": "delete", "path": path})
        self.db.pop(path)
        return True

    def list_files(self, path: str, recursive: bool = False) -> list[str]:
        self.log.append({"func": "list_files", "path": path, "recursive": recursive})
        return list(self.db[path].keys())
