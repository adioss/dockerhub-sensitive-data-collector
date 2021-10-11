import logging

from dockerhub.result import Result
from utils.config import Config


def write_result(sensitive_data: Result):
    """ Write results to output path """
    output: str = f"{sensitive_data.repository}:{sensitive_data.tag} : {sensitive_data.to_json()}"
    logging.info(output)
    with open(Config.get_instance().output_path(), "a", encoding="utf-8") as output_file:
        output_file.write(f"{output}\n")
