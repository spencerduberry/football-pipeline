import attrs
from attrs.validators import ge, instance_of, lt, matches_re, max_len, min_len


@attrs.define
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
