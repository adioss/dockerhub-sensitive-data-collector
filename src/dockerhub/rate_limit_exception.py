from typing import Final

RATE_LIMIT_EXCEEDED_MESSAGE: Final = "Rate limit exceeded"


class RateLimitException(Exception):
    pass
