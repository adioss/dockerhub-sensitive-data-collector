import argparse
import logging
import time

from dockerhub.puller import list_last_updated_image


def main():
    """ main """
    parser = argparse.ArgumentParser(description='Collect sensitive from Dockerhub related to last pushed '
                                                 'Docker images')
    # parser.add_argument('--configuration-file', type=int, required=True, help='Configuration file')
    parser.add_argument("--log-level", default=logging.INFO, type=lambda x: getattr(logging, x),
                        help="Configure the logging level.")
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level)
    currently_parsed_elements = []
    logging.info("Starting the application using log-level: %s", args.log_level)
    while True:
        currently_parsed_elements = list_last_updated_image(currently_parsed_elements)
        time.sleep(5)
        # TODO WTH
        if len(currently_parsed_elements) == 1000:
            currently_parsed_elements = []


if __name__ == '__main__':
    main()
