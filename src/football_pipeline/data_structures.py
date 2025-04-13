"""Module for data models."""

from datetime import date, datetime

import attrs
from attrs.validators import ge, in_, instance_of, matches_re


def parse_date(value):
    value = value[:10]
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


player_status = [
    "a",
    "d",
    "i",
    "u",
]


@attrs.define
class BronzePlayer:
    player_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
    team_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
    player_type: int = attrs.field(
        validator=[instance_of(int), in_(range(1, 5))], converter=int
    )
    first_name: str = attrs.field(
        validator=[instance_of(str), matches_re(r"^[\D\s]+$")], converter=str.title
    )
    second_name: str = attrs.field(
        validator=[instance_of(str), matches_re(r"^[\D\s]+$")], converter=str.title
    )
    status: str = attrs.field(
        validator=[instance_of(str), in_(player_status)],
        converter=str.lower,
    )
    birth_date: date = attrs.field(validator=[instance_of(date)], converter=parse_date)


@attrs.define
class BronzeFixture:
    fixture_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
    started: bool = attrs.field(validator=instance_of(bool))
    finished: bool = attrs.field(validator=instance_of(bool))
    kickoff_time: date = attrs.field(
        validator=[instance_of(date)], converter=parse_date
    )
    home_team_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
    away_team_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
    team_h_difficulty: int = attrs.field(
        validator=[instance_of(int), ge(0)], converter=int
    )
    team_a_difficulty: int = attrs.field(
        validator=[instance_of(int), ge(0)], converter=int
    )


@attrs.define
class BronzeStats:
    event_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
    team_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
    fixture_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
    player_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
