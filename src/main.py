import argparse
import logging
import time

from dockerhub.puller import list_last_updated_image
from utils.config import Config


def main():
    """ main """
    parser = argparse.ArgumentParser(description='Collect sensitive from Dockerhub related to last pushed '
                                                 'Docker images')
    parser.add_argument('--configuration-file', type=str, required=False, help='Config file')
    parser.add_argument("--log-level", default=logging.INFO, type=lambda x: getattr(logging, x),
                        help="Configure the logging level.")
    config = Config.get_instance(parser=parser)
    logging.info("Starting the application: %s, %s", config.log_level(), config.output_path())
    currently_parsed_elements = []
    while True:
        currently_parsed_elements = list_last_updated_image(currently_parsed_elements)
        time.sleep(5)
        # TODO WTH
        if len(currently_parsed_elements) == 1000:
            currently_parsed_elements = []


if __name__ == '__main__':
    main()
