from typing import Final

RATE_LIMIT_EXCEEDED_MESSAGE: Final = "RATE LIMIT EXCEEDED"


class RateLimitException(Exception):
    pass
