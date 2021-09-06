from typing import Final

RATE_LIMIT_EXCEEDED_MESSAGE: Final = "rate limit exceeded"


class RateLimitException(Exception):
    """ Rate limit exceeded exception """
