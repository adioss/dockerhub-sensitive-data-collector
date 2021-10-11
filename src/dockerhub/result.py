import json
from datetime import datetime

from unconcealment.secret_pattern import SecretPattern


class Result:
    """ Convert object to json """
    repository: str
    tag: str
    pattern: SecretPattern
    value: str
    layer: str

    def __init__(self, repository: str, tag: str, pattern: SecretPattern, value: str, layer: str):
        self.date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f %Z")
        self.repository = repository
        self.tag = tag
        self.pattern = pattern
        self.value = value
        self.layer = layer

    def to_json(self) -> str:
        """ Convert object to json """
        return json.dumps(self.__dict__, default=str)
