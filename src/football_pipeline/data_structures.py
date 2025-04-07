import attrs
from attrs.validators import gt, in_, instance_of, matches_re, max_len, min_len


@attrs.define
class TeamsTable:
    team_id: int = attrs.field(validator=[instance_of(int), gt(0)], converter=int)
    name: str = attrs.field(validator=[instance_of(str), min_len(2), max_len(100)])
    position: int = attrs.field(
        validator=[instance_of(int), in_(range(1, 21))], converter=int
    )
    short_name: str = attrs.field(
        validator=[instance_of(str), matches_re("[A-Z]{3}")], converter=[str, str.upper]
    )


@attrs.define
class Event:
    event_id: int = attrs.field(validator=[instance_of(int), gt(0)], converter=int)
    event: str = attrs.field(validator=[instance_of(str), min_len(2), max_len(100)])


@attrs.define
class PlayerMatchStats:
    player_id: int = attrs.field(validator=[instance_of(int), gt(0)], converter=int)
    fixture_id: int = attrs.field(validator=[instance_of(int), gt(0)], converter=int)
    minutes_played: int = attrs.field(validator=[instance_of(int)], converter=int)
    influence: float = attrs.field(validator=[instance_of(float)], converter=float)
    creativity: float = attrs.field(validator=[instance_of(float)], converter=float)
    threat: float = attrs.field(validator=[instance_of(float)], converter=float)
    ict_index: float = attrs.field(validator=[instance_of(float)], converter=float)
    starts: int = attrs.field(validator=[instance_of(int)], converter=int)
    expeected_goals: float = attrs.field(
        validator=[instance_of(float)], converter=float
    )
    expected_assists: float = attrs.field(
        validator=[instance_of(float)], converter=float
    )
    expected_goal_involvements: float = attrs.field(
        validator=[instance_of(float)], converter=float
    )
    expected_goals_conceded: float = attrs.field(
        validator=[instance_of(float)], converter=float
    )
