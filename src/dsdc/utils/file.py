import logging

from dsdc.dockerhub.result import Result
from dsdc.utils.config import Config


def write_result(sensitive_data: Result):
    """ Write results to output path """
    logging.info("%s:%s : %s", sensitive_data.repository, sensitive_data.tag, sensitive_data.to_json())
    with open(Config.output_path(), "a", encoding="utf-8") as output_file:
        output_file.write(f"{sensitive_data.to_json()}\n")
