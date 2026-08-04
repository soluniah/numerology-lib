from typing import TypedDict


class FactorValue(TypedDict):
    master: int
    karmic: int
    value: int


class DivisibleValue(TypedDict):
    soul: int
    karma: int


Period = TypedDict(
    "Period",
    {
        "from": int,
        "to": float,
        "achievement": int,
        "challenge": int,
    },
)
