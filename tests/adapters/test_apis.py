import inspect

import pytest

from football_pipeline.adapters.fs_wrapper import FakeFSLocal, FSLocal
from football_pipeline.adapters.io_wrapper import FakeIOWrapper, IOWrapper
from football_pipeline.adapters.logger import FakeLogger, RealLogger


def get_signatures(entity: object) -> dict[str, inspect.Signature]:
    return {
        name: inspect.signature(func)
        for name, func in inspect.getmembers(entity, inspect.isroutine)
        if not (name.startswith("__") and name.endswith("__"))
    }


class SanityCheck:
    def method(type1: int, type2: float) -> float:
        return type1**type2


class FakeMissingMethod:
    pass


class FakeAdditionalMethod:
    def method(type1: int, type2: float) -> float:
        return type1**type2

    def test_method(test: str) -> str:
        return test


class FakeWrongSignature:
    def method(type1: int, type2: int) -> float:
        return type1**type2


@pytest.mark.parametrize(
    "real, fake",
    [
        pytest.param(
            SanityCheck(),
            FakeAdditionalMethod(),
            id="Ensuring all methods in a real are in a fake.",
        ),
        pytest.param(
            SanityCheck(),
            FakeMissingMethod(),
            id="Ensuring it will fail if methods out of sync.",
            marks=pytest.mark.xfail(
                reason="Ensuring it will fail if methods out of sync.", strict=True
            ),
        ),
        pytest.param(
            SanityCheck(),
            FakeWrongSignature(),
            id="Ensuring it will fail if method signature is misaligned.",
            marks=pytest.mark.xfail(
                reason="Ensuring it will fail if method signature is misaligned.",
                strict=True,
            ),
        ),
        pytest.param(
            FSLocal(),
            FakeFSLocal(),
            id="Ensuring all methods in the file system wrapper match.",
        ),
        pytest.param(
            IOWrapper(),
            FakeIOWrapper(),
            id="Ensuring all methods in the IO wrapper match.",
        ),
        pytest.param(
            RealLogger("test"),
            FakeLogger("test"),
            id="Ensuring all methods in the logger match.",
        ),
    ],
)
def test_fake_apis(real, fake):
    fake_methods = get_signatures(fake)
    real_methods = get_signatures(real)
    mismatches = [
        {
            "method_name": name,
            "real_signature": func,
            "fake_signature": fake_methods.get(name),
        }
        for name, func in real_methods.items()
        if fake_methods.get(name) != func
    ]
    assert mismatches == []
