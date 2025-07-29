import datetime
import uuid


def time_now(date_format: str = "%Y%m%d_%H%M%S") -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime(date_format)


def fake_time_now(date_format: str = "%Y%m%d_%H%M%S") -> str:
    return datetime.datetime(
        2025, 4, 25, 23, 23, 55, tzinfo=datetime.timezone.utc
    ).strftime(date_format)


def new_guid() -> str:
    return str(uuid.uuid4())


def fake_new_guid() -> str:
    return "123432424-absdbfdf"
