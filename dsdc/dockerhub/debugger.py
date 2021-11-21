from unconcealment.finder import extract_secret
from unconcealment.secret_pattern import SecretPattern


def debug_from_file(file_path: str):
    """ main """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            try:
                split = line.split(" : ")
                content = split[2]
                pattern = extract_secret(content, SecretPattern.AZURE_CLIENT_ID)
                if pattern:
                    # pylint: disable=W0703
                    print(f"{split[0]}:{split[1]}"
                          f" (https://hub.docker.com/r/{split[0]}/tags?page=1&ordering=last_updated) : {content}")
            # pylint: disable=W0702
            except:
                print(f"!!!! Cannot be parsed: {line}")
