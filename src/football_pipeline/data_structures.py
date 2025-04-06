import attrs
from attrs.validators import in_, instance_of

teams = [
    "Arsenal",
    "Aston Villa",
    "Bournemouth",
    "Brentford",
    "Brighton",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Ipswich",
    "Leicester",
    "Liverpool",
    "Man City",
    "Man Utd",
    "Newcastle",
    "Nott'm Forest",
    "Southampton",
    "Spurs",
    "West Ham",
    "Wolves",
]


def is_length_3(instance, attribute, value):
    if not isinstance(value, str):
        raise TypeError(
            f"'{attribute.name}' must be a string (got {type(value).__name__})"
        )
    if len(value) != 3:
        raise ValueError(
            f"'{attribute.name}' must be exactly 3 characters long (got {len(value)})"
        )


def all_caps(instance, attribute, value):
    if not isinstance(value, str):
        raise TypeError(
            f"'{attribute.name}' must be a string (got {type(value).__name__})"
        )
    if not value.isupper():
        raise ValueError(
            f"'{attribute.name}' must contain only uppercase letters (got '{value}')"
        )


@attrs.define
class TeamsTable:
    team_id: int = attrs.field(validator=[instance_of(int), in_(range(1, 21))])
    name: str = attrs.field(validator=[instance_of(str), in_(teams)])
    position: int = attrs.field(validator=[instance_of(int), in_(range(1, 21))])
    short_name: str = attrs.field(validator=[instance_of(str), is_length_3, all_caps])
    strength: int = attrs.field(validator=[instance_of(int)])
