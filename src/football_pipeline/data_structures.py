"""Module for data models."""

from datetime import date, datetime

import attrs
from attrs.validators import ge, in_, instance_of, lt, matches_re, max_len, min_len


def parse_date(value):
    if isinstance(value, date):
        return value
    value = value[:10]
    return datetime.strptime(value, "%Y-%m-%d").date()


PLAYER_STATUS = [
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
        validator=[instance_of(str), matches_re(r"^[\D\s]+$")], converter=str.lower
    )
    second_name: str = attrs.field(
        validator=[instance_of(str), matches_re(r"^[\D\s]+$")], converter=str.lower
    )
    status: str = attrs.field(
        validator=[instance_of(str), in_(PLAYER_STATUS)],
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


class BronzeTeams:
    team_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
    name: str = attrs.field(validator=[instance_of(str), min_len(2), max_len(100)])
    position: int = attrs.field(
        validator=[instance_of(int), ge(1), lt(21)], converter=int
    )
    short_name: str = attrs.field(
        validator=[instance_of(str), matches_re("[A-Z]{3}")], converter=[str, str.upper]
    )


@attrs.define
class BronzeEvent:
    event_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
    event: str = attrs.field(validator=[instance_of(str), min_len(2), max_len(100)])


@attrs.define
class BronzePlayerMatchStats:
    player_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
    fixture_id: int = attrs.field(validator=[instance_of(int), ge(1)], converter=int)
    minutes_played: int = attrs.field(
        validator=[instance_of(int), ge(0)], converter=int
    )
    influence: float = attrs.field(
        validator=[instance_of(float), ge(0)], converter=float
    )
    creativity: float = attrs.field(
        validator=[instance_of(float), ge(0)], converter=float
    )
    threat: float = attrs.field(validator=[instance_of(float), ge(0)], converter=float)
    ict_index: float = attrs.field(
        validator=[instance_of(float), ge(0)], converter=float
    )
    starts: int = attrs.field(validator=[instance_of(int), ge(0)], converter=int)
    expeected_goals: float = attrs.field(
        validator=[instance_of(float), ge(0)], converter=float
    )
    expected_assists: float = attrs.field(
        validator=[instance_of(float), ge(0)], converter=float
    )
    expected_goal_involvements: float = attrs.field(
        validator=[instance_of(float), ge(0)], converter=float
    )
    expected_goals_conceded: float = attrs.field(
        validator=[instance_of(float), ge(0)], converter=float
    )
