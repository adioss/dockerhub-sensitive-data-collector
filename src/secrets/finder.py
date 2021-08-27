from typing import Final

from src.secrets.pattern import Pattern

MAX_TESTED_LENGTH: Final = 5000


def contains_secret_pattern(tested: str, matcher: Pattern) -> bool:
    """ Check if a string contains a secret using regexp"""
    if len(tested) == 0:
        return False
    for i in range(0, len(tested), MAX_TESTED_LENGTH):
        value = tested[i:i + MAX_TESTED_LENGTH]
        result = matcher.value.match(value)
        if result is None:
            return False
    return True
