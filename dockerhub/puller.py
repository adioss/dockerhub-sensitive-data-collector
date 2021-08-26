import json
import logging

import requests
from retrying import retry

from dockerhub.result import Result
from secrets import finder
from secrets.finder import Pattern
from utils.contants import DOCKERHUB_URL, DOCKERHUB_SEARCH_URL, SEARCH_PAGE_SIZE
from utils.utils import sha256


def compute_repository(repository: str) -> str:
    """ TODO """
    repository = repository.replace(" ", "-")
    return repository if "/" in repository else "library/" + repository


def collect_sensitive_data_from_layers(layers: list) -> list:
    """ TODO """
    results = []
    for layer in layers:
        logging.debug("Layer: %s", layer)
        for pattern in Pattern:
            if finder.contains_secret_pattern(layer['instruction'], pattern):
                logging.debug("Secret found: %s" % layer)
                results.append(Result(pattern, layer))
    return results


@retry(wait_fixed=10000)
def collect_layers(repository: str, tag: dict) -> list:
    """ TODO """
    logging.debug("Tags: %s (on repository %s)", tag["name"], repository)
    query = "%s/v2/repositories/%s/tags/%s/images" % (DOCKERHUB_URL, repository, tag["name"])
    logging.debug("Layers url: %s", query)
    headers = {'Search-Version': 'v3', 'Content-Type': 'application/json'}
    response = requests.request("GET", query, headers=headers, data={})
    return json.loads(response.text)[0]['layers']


@retry(wait_fixed=10000)
def parse_tags(repository: str):
    """ TODO """
    query = "%s/v2/repositories/%s/tags?page=1&page_size=1&ordering=last_updated" % (DOCKERHUB_URL, repository)
    logging.debug("Tags url: %s", query)
    headers = {'Search-Version': 'v3', 'Content-Type': 'application/json'}
    response = requests.request("GET", query, headers=headers, data={})
    tags = json.loads(response.text)
    if tags["count"] > 0:
        collected = collect_sensitive_data_from_layers(collect_layers(repository, tags["results"][0]))
        if len(collected) > 0:
            for sensitive_data in collected:
                logging.info("%s : %s" % (repository, sensitive_data.to_json()))


def parse_repository(summary: dict):
    """ TODO """
    logging.debug("Image to parse: %s", summary["name"])
    repository = compute_repository(summary["name"])
    parse_tags(repository)


@retry(wait_fixed=10000)
def list_last_updated_image(currently_parsed_elements: list) -> list:
    """ List last updated images """
    page = "1"
    query = "%s?q=&type=image&tag&sort=updated_at&order=desc&page_size=%s&page=%s" \
            % (DOCKERHUB_SEARCH_URL, SEARCH_PAGE_SIZE, page)
    headers = {'Search-Version': 'v3', 'Content-Type': 'application/json'}
    response = requests.request("GET", query, headers=headers, data={})
    logging.debug("Last pushed images (page %s) : %s", str(page), response.text)
    summaries = json.loads(response.text)["summaries"]
    for summary in summaries:
        computed = sha256(summary)
        if computed in currently_parsed_elements:
            logging.debug("Already parsed: %s", computed)
            return currently_parsed_elements
        parse_repository(summary)
        currently_parsed_elements.append(computed)
    return currently_parsed_elements
