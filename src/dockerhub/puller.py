import json
import logging
import traceback

import requests
from retrying import retry

from dockerhub.rate_limit_exception import RateLimitException, RATE_LIMIT_EXCEEDED_MESSAGE
from dockerhub.result import Result
from secrets import finder
from secrets.finder import Pattern
from utils.contants import DOCKERHUB_URL, DOCKERHUB_SEARCH_URL, SEARCH_PAGE_SIZE
from utils.utils import sha256


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
    if response.status_code != 200:
        logging.info(response.status_code)
    if response.status_code == 404 or response.status_code == 500:
        return dict()
    loads = json.loads(response.text)
    if 'detail' in loads and loads['detail'] == RATE_LIMIT_EXCEEDED_MESSAGE:
        raise RateLimitException
    return loads


def compute_repository(repository: str) -> str:
    """ TODO """
    repository = repository.replace(" ", "-")
    return repository if "/" in repository else "library/" + repository


def collect_sensitive_data_from_tag(repository: str, tag: dict) -> list:
    """ TODO """
    layers: list = collect_layers(repository, tag)
    results = []
    for layer in layers:
        for pattern in Pattern:
            if finder.contains_secret_pattern(layer['instruction'], pattern):
                results.append(Result(repository, pattern, layer))
    return results


def collect_layers(repository: str, tag: dict) -> list:
    """ TODO """
    query = "%s/v2/repositories/%s/tags/%s/images" % (DOCKERHUB_URL, repository, tag['name'])
    logging.debug("Tags: %s (on repository %s), Layers url: %s ", tag['name'], repository, query)
    response = get_request(query)
    if len(response) == 0 or 'layers' not in response[0]:
        return []
    return response[0]['layers']


def parse_tags(repository: str):
    """ TODO """
    query = "%s/v2/repositories/%s/tags?page=1&page_size=1&ordering=last_updated" % (DOCKERHUB_URL, repository)
    logging.debug("Tags url: %s", query)
    tags = get_request(query)
    if bool(tags):
        return
    if 'count' in tags and tags['count'] > 0:
        collected = collect_sensitive_data_from_tag(repository, tags['results'][0])
        if len(collected) > 0:
            for sensitive_data in collected:
                logging.info("%s : %s", repository, sensitive_data.to_json())


def parse_repository(summary: dict):
    """ TODO """
    logging.debug("Image to parse: %s", summary['name'])
    repository = compute_repository(summary['name'])
    parse_tags(repository)


def list_last_updated_image(currently_parsed_elements: list) -> list:
    """ List last updated images """
    # TODO loop instead of '1'
    page = "1"
    query = "%s?q=&type=image&tag&sort=updated_at&order=desc&page_size=%s&page=%s" \
            % (DOCKERHUB_SEARCH_URL, SEARCH_PAGE_SIZE, page)
    summaries = get_request(query)['summaries']
    for summary in summaries:
        computed = sha256(summary)
        if computed in currently_parsed_elements:
            logging.debug("Already parsed: %s", computed)
            return currently_parsed_elements
        parse_repository(summary)
        currently_parsed_elements.append(computed)
    return currently_parsed_elements
