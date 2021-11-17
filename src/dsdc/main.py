import argparse
import logging
import time

from dsdc.dockerhub.puller import list_last_updated_image, parse_tag
from dsdc.utils.config import Config


def main():
    """ main """
    parser = argparse.ArgumentParser(description='Collect sensitive from Dockerhub related to last pushed '
                                                 'Docker images')
    parser.add_argument('-o', '--output-path', type=str, required=False, help='Output path')
    parser.add_argument('-t', '--tag', type=str, required=False, help='Check a specific image:tag')
    parser.add_argument('-f', '--filter', type=str, required=False, help='Filter specific image:tag using regexp')
    parser.add_argument('-l', '--log-level', default=logging.INFO, type=lambda x: getattr(logging, x),
                        help="Configure the logging level.")
    Config.init(parser)
    logging.info("Starting the application: %s, %s", Config.log_level(), Config.output_path())

    currently_parsed_elements = []
    if Config.tag() is not None:
        config_tag_split = Config.tag().split(":", 1)
        parse_tag(config_tag_split[0], config_tag_split[1])
        exit(0)
    while True:
        currently_parsed_elements = list_last_updated_image(currently_parsed_elements)
        time.sleep(5)
        # TODO WTH
        if len(currently_parsed_elements) == 1000:
            currently_parsed_elements = []


if __name__ == '__main__':
    main()
