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
    strength: int = attrs.field(validator=[instance_of(int)], converter=int)
