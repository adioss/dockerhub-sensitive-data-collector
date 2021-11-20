import logging

from dockerhub.result import Result
from unconcealment import finder
from unconcealment.secret_pattern import SecretPattern
from utils.config import Config
from utils.contants import DOCKERHUB_URL, DOCKERHUB_SEARCH_URL, SEARCH_PAGE_SIZE
from utils.file import write_result
from utils.http import get_request
from utils.utils import sha256


def compute_repository(repository: str) -> str:
    """ TODO """
    repository = repository.replace(" ", "-")
    return repository if "/" in repository else "library/" + repository


def collect_layers(repository: str, tag: str) -> list:
    """ TODO """
    query = f"{DOCKERHUB_URL}/v2/repositories/{repository}/tags/{tag}/images"
    logging.debug("Tags: %s (on repository %s), Layers url: %s ", tag, repository, query)
    response = get_request(query)
    if len(response) == 0 or 'layers' not in response[0]:
        return []
    return response[0]['layers']


def parse_tags(repository: str):
    """ TODO """
    query = f"{DOCKERHUB_URL}/v2/repositories/{repository}/tags?page=1&page_size=1&ordering=last_updated"
    logging.debug("Tags url: %s", query)
    tags = get_request(query)
    if not bool(tags):
        return
    if 'count' in tags and tags['count'] > 0:
        tag_name = tags['results'][0]['name']
        # if no regexp or if regexp match something
        if (Config.regexp() is None or
                (Config.regexp() is not None and Config.regexp().match(f"{repository}/{tag_name}") is not None)):
            logging.info("Tag to parse: %s:%s", repository, tag_name)
            write_result(collect_sensitive_data_from_tag(repository, tag_name))


def collect_sensitive_data_from_tag(repository, tag):
    """ TODO """
    layers: list = collect_layers(repository, tag)
    results = []
    for layer in layers:
        for secret_pattern in SecretPattern:
            secret = finder.extract_secret(layer['instruction'], secret_pattern)
            if secret is not None:
                results.append(Result(repository, tag, secret_pattern, secret, layer))
    return results


def parse_repository(summary: dict):
    """ TODO """
    repository = compute_repository(summary['name'])
    parse_tags(repository)


def list_last_updated_image(currently_parsed_elements: list) -> list:
    """ List last updated images """
    # TODO loop instead of '1'
    page = "1"
    query = f"{DOCKERHUB_SEARCH_URL}?q=&type=image&tag&sort=updated_at&order=desc&page_size={SEARCH_PAGE_SIZE}" \
            f"&page={page}"
    summaries = get_request(query)['summaries']
    for summary in summaries:
        computed = sha256(summary)
        if computed in currently_parsed_elements:
            logging.debug("Already parsed: %s", computed)
            return currently_parsed_elements
        parse_repository(summary)
        currently_parsed_elements.append(computed)
    return currently_parsed_elements
