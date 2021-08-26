import json

from secrets.finder import Pattern


class Result:
    pattern: Pattern
    value: str

    def __init__(self, pattern: Pattern, value: str):
        self.pattern = pattern
        self.value = value

    def to_json(self) -> str:
        return json.dumps(self.__dict__, default=str)