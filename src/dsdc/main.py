import argparse
import logging
import re

from unconcealment.finder import extract_secret
from unconcealment.secret_pattern import SecretPattern

from dsdc.utils.config import Config


def clean():
    with open(
            '/Users/apailhes/Library/Application Support/JetBrains/IntelliJIdea2021.2/scratches/AZURE_CLIENT_SECRET.txt',
            'r') as file:
        result = []
        lines = file.readlines()
        for line in lines:
            line = re.sub(r'.*AZURE_CLIENT_SECRET : ', '', line)
            result.append(line)
        with open(
                '/Users/apailhes/Library/Application Support/JetBrains/IntelliJIdea2021.2/scratches/AZURE_CLIENT_SECRET2.txt',
                'w') as file2:
            file2.writelines(result)


def debug_from_file():
    """ main """
    with open(
            '/Users/apailhes/Library/Application Support/JetBrains/IntelliJIdea2021.2/scratches/AZURE_CLIENT_SECRET.txt',
            'r') as file:
        lines = file.readlines()
        for line in lines:
            try:
                split = line.split(" : ")
                content = split[2]
                pattern = extract_secret(content, SecretPattern.AZURE_CLIENT_ID)
                if pattern:
                    # pylint: disable=W0703
                    print("%s:%s (https://hub.docker.com/r/%s/tags?page=1&ordering=last_updated) : %s" % (
                        split[0], split[1], split[0], content))
            except:
                print("!!!! Cannot be parsed: %s" % line)


def main():
    """ main """
    parser = argparse.ArgumentParser(description='Collect sensitive from Dockerhub related to last pushed '
                                                 'Docker images')
    parser.add_argument('--configuration-file', type=str, required=False, help='Config file')
    parser.add_argument("--log-level", default=logging.INFO, type=lambda x: getattr(logging, x),
                        help="Configure the logging level.")
    Config.init(parser)
    logging.info("Starting the application: %s, %s", Config.log_level(), Config.output_path())
    # currently_parsed_elements = []
    # while True:
    #     currently_parsed_elements = list_last_updated_image(currently_parsed_elements)
    #     time.sleep(5)
    #     # TODO WTH
    #     if len(currently_parsed_elements) == 1000:
    #         currently_parsed_elements = []

    # clean()
    # debug_from_file()


if __name__ == '__main__':
    main()
