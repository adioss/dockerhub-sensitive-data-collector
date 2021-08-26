import enum
import re
from typing import Final

MAX_TESTED_LENGTH: Final = 5000


class Pattern(enum.Enum):
    """ Regexp pattern for secret detection """
    # //    FACEBOOK_KEY=.*(((?i)fb(.{0,20}))|((?i)facebook(.{0,20}))).*"
    AWS_CREDENTIAL_FILE = re.compile(".*credentials.*")
    AWS_KEY = re.compile(".*(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA).*")
    AWS_SECRET = re.compile(".*(AWS|aws).*([A-Za-z0-9/+=]{40}){1}")
    AZURE_CLIENT_SECRET = re.compile(".*((?i)([0-9A-Fa-f]{4}-){4}[0-9A-Fa-f]{12}?).*")
    TWITTER_KEY = re.compile(".*((?i)twitter(.{0,20})).*")
    GITHUB_KEY = re.compile(".*((?i)(ghu|ghs|gho|ghp)_[0-9a-zA-Z]{36}).*")
    GCP_KEY = re.compile(".*((?i)AIza).*")
    GCP_SERVICE_ACCOUNT = re.compile(".*((?i)service_account).*")
    HEROKU_KEY = re.compile(".*((?i)heroku).*")
    SHOPIFY_KEY = re.compile(".*((?i)(shpss|shpat|shpca|shppa)_[a-fA-F0-9]{32}).*")
    PIPY_KEY = re.compile(".*((?i)(pypi-AgEIcHlwaS5vcmc)).*")


def contains_secret_pattern(tested: str, matcher: Pattern) -> bool:
    """ Check if a string contains a secret using regexp"""
    for i in range(0, len(tested), MAX_TESTED_LENGTH):
        value = tested[i:i + MAX_TESTED_LENGTH]
        result = matcher.value.match(value)
        if result is None:
            return False
    return True
