import json
import logging

import requests

from utils.contants import DOCKERHUB_URL, DOCKERHUB_SEARCH_URL, SEARCH_PAGE_SIZE
from utils.utils import sha256


def compute_repository(repository: str):
    """ TODO """
    repository = repository.replace(" ", "-")
    return repository if "/" in repository else "library/" + repository


def collect_sensitive_data_from_layers(layers: list):
    """ TODO """
    for layer in layers:
        logging.debug("Layer: %s", layer)


def collect_layers(repository: str, tag: dict):
    """ TODO """
    logging.debug("Tags: %s (on repository %s)", tag["name"], repository)
    query = "%s/v2/repositories/%s/tags/%s/images" % (DOCKERHUB_URL, repository, tag["name"])
    logging.debug("Layers url: %s", query)
    headers = {'Search-Version': 'v3', 'Content-Type': 'application/json'}
    response = requests.request("GET", query, headers=headers, data={})
    return json.loads(response.text)[0]['layers']


def parse_tags(repository: str):
    """ TODO """
    query = "%s/v2/repositories/%s/tags?page=1&page_size=1&ordering=last_updated" % (DOCKERHUB_URL, repository)
    logging.debug("Tags url: %s", query)
    headers = {'Search-Version': 'v3', 'Content-Type': 'application/json'}
    response = requests.request("GET", query, headers=headers, data={})
    tags = json.loads(response.text)
    if tags["count"] > 0:
        collect_sensitive_data_from_layers(collect_layers(repository, tags["results"][0]))


def parse_repository(summary: dict):
    """ TODO """
    logging.debug("Image to parse: %s", summary["name"])
    repository = compute_repository(summary["name"])
    parse_tags(repository)


def list_last_updated_image(currently_parsed_elements: list):
    """ TODO """
    page = "1"
    query = "%s?q=&type=image&tag&sort=updated_at&order=desc&page_size=%s&page=%s" \
            % (DOCKERHUB_SEARCH_URL, SEARCH_PAGE_SIZE, page)
    headers = {'Search-Version': 'v3', 'Content-Type': 'application/json'}
    response = requests.request("GET", query, headers=headers, data={})
    logging.debug("Last pushed images (page %s) : %s", str(page), response.text)
    summaries = json.loads(response.text)["summaries"]
    for index, summary in enumerate(summaries):
        computed = sha256(summary)
        if computed in currently_parsed_elements:
            logging.debug("Already parsed: %s", computed)
            return currently_parsed_elements
        parse_repository(summary)
        currently_parsed_elements.append(computed)
    return currently_parsed_elements
