import json
import logging
import traceback
from typing import Final

import requests
from retrying import retry
from utils.rate_limit_exception import RateLimitException, RATE_LIMIT_EXCEEDED_MESSAGE

UNMANAGED_RESPONSE_CODE: Final = [403, 404, 500]


def retry_if_io_error(exception):
    """ TODO """
    if isinstance(exception, RateLimitException):
        return True
    logging.error(traceback.print_tb(exception.__traceback__))
    return False


@retry(wait_fixed=10000, retry_on_exception=retry_if_io_error)
def get_request(query) -> dict:
    """ TODO """
    headers = {'Search-Version': 'v3', 'Content-Type': 'application/json'}
    response = requests.request("GET", query, headers=headers, data={}, stream=False)
    if response.status_code in UNMANAGED_RESPONSE_CODE:
        logging.debug("Unmanaged response: %s (for query %s)", response.status_code, query)
        return {}
    if response.status_code != 200:
        logging.warning("Unknown response: %s (for query %s)", response.status_code, query)
        return {}
    loads = json.loads(response.text)
    if 'detail' in loads and loads['detail'].lower() == RATE_LIMIT_EXCEEDED_MESSAGE:
        raise RateLimitException
    return loads
