import json

from secrets.finder import Pattern


class Result:
    """ Convert object to json """
    repository: str
    pattern: Pattern
    value: str

    def __init__(self, repository: str, pattern: Pattern, value: str):
        self.repository = repository
        self.pattern = pattern
        self.value = value

    def to_json(self) -> str:
        """ Convert object to json """
        return json.dumps(self.__dict__, default=str)
