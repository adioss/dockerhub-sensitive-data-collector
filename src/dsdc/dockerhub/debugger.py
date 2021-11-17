from unconcealment.finder import extract_secret
from unconcealment.secret_pattern import SecretPattern


def debug_from_file(file_path: str):
    """ main """
    with open(file_path, 'r') as file:
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
