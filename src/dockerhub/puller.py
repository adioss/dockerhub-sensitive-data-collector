import logging

from dockerhub.result import Result
from secrets import finder
from secrets.finder import SecretPattern
from utils.contants import DOCKERHUB_URL, DOCKERHUB_SEARCH_URL, SEARCH_PAGE_SIZE
from utils.file import write_result
from utils.http import get_request
from utils.utils import sha256


def compute_repository(repository: str) -> str:
    """ TODO """
    repository = repository.replace(" ", "-")
    return repository if "/" in repository else "library/" + repository


def collect_sensitive_data_from_tag(repository: str, tag: dict) -> list:
    """ TODO """
    layers: list = collect_layers(repository, tag)
    results = []
    for layer in layers:
        for secret_pattern in SecretPattern:
            if finder.contains_secret_pattern(layer['instruction'], secret_pattern):
                results.append(Result(repository, tag['name'], secret_pattern, layer))
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
    if not bool(tags):
        return
    if 'count' in tags and tags['count'] > 0:
        collected = collect_sensitive_data_from_tag(repository, tags['results'][0])
        if len(collected) > 0:
            for sensitive_data in collected:
                write_result(sensitive_data)


def parse_repository(summary: dict):
    """ TODO """
    logging.info("Image to parse: %s", summary['name'])
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
