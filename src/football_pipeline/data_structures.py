"""Module for data models."""

from datetime import date

import attrs
from attrs.validators import instance_of, matches_re, max_len


@attrs.define
class Player:
    player_id: int = attrs.field(validator=instance_of(int), converter=int)
    team_id: int = attrs.field(validator=[instance_of(int), max_len(2)], converter=int)
    player_type: int = attrs.field(
        validator=[instance_of(int), max_len(1), range(1, 4)], converter=int
    )
    first_name: str = attrs.field(
        validator=[instance_of(str), matches_re(r"^[\D\s]+$")], converter=str.title
    )
    second_name: str = attrs.field(
        validator=[instance_of(str), matches_re(r"^[\D\s]+$")], converter=str.title
    )
    status: str = attrs.field(
        validator=[instance_of(str), max_len(1), matches_re(r"^[a-zA-Z]$")],
        converter=str.lower,
    )
    birth_date: date = attrs.field(validator=[instance_of(date)], converter=date)
