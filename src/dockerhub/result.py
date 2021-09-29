import json

from secrets.secret_pattern import SecretPattern


class Result:
    """ Convert object to json """
    repository: str
    tag: str
    pattern: SecretPattern
    value: str

    def __init__(self, repository: str, tag: str, pattern: SecretPattern, value: str):
        self.repository = repository
        self.tag = tag
        self.pattern = pattern
        self.value = value

    def to_json(self) -> str:
        """ Convert object to json """
        return json.dumps(self.__dict__, default=str)
