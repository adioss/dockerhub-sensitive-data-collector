import logging
from typing import List

from dsdc.utils.config import Config


def write_result(sensitive_contents: List):
    """ Write results to output path """
    if len(sensitive_contents) > 0:
        for sensitive_content in sensitive_contents:
            logging.info("%s:%s : %s", sensitive_content.repository, sensitive_content.tag, sensitive_content.to_json())
            if Config.output_path() is not None:
                with open(Config.output_path(), "a", encoding="utf-8") as output_file:
                    output_file.write(f"{sensitive_content.to_json()}\n")
