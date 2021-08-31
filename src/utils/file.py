import logging

from dockerhub.result import Result
from utils.config import Config


def write_result(repository: str, sensitive_data: Result):
    """ Write results to output path """
    output: str = "%s : %s" % (repository, sensitive_data.to_json())
    logging.info(output)
    with open(Config.get_instance().output_path(), "a") as output_file:
        output_file.write("%s\n" % output)
