from typing import Callable

import attrs

from football_pipeline.adapters.fs_wrapper import FSProtocol
from football_pipeline.adapters.io_wrapper import IOProtocol
from football_pipeline.adapters.logger import LoggerProtocol


@attrs.define
class Repo:
    io: IOProtocol = attrs.field(validator=attrs.validators.instance_of(IOProtocol))
    fs: FSProtocol = attrs.field(validator=attrs.validators.instance_of(FSProtocol))
    logger: LoggerProtocol = attrs.field(
        validator=attrs.validators.instance_of(LoggerProtocol)
    )
    time_func: Callable = attrs.field(validator=attrs.validators.instance_of(Callable))
    guid_func: Callable = attrs.field(validator=attrs.validators.instance_of(Callable))

    def __attrs_post_init__(self) -> None:
        self.logger.setup()
