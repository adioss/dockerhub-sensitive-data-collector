import base64
import hashlib
import json


def sha256(value: dict):
    """ Compute hash (sha256) of a dictionary """
    algo = hashlib.sha256()
    algo.update(bytes("%s" % json.dumps(value), "utf-8"))
    return str(base64.b64encode(algo.digest()))
