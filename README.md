# Dockerhub Sensitive Data Collector

Collect sensitive data leaked in docker images hosted in [https://hub.docker.com/](https://hub.docker.com/) (AWS, GCP or
AZURE keys, NPM tokens etc...) using [unconcealment python library](https://github.com/adioss/unconcealment).

## Badges

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![ci](https://github.com/adioss/dockerhub-sensitive-data-collector/actions/workflows/ci.yml/badge.svg)](https://github.com/adioss/dockerhub-sensitive-data-collector/actions/workflows/ci.yml)
[![cd](https://github.com/adioss/dockerhub-sensitive-data-collector/actions/workflows/cd.yml/badge.svg)](https://github.com/adioss/dockerhub-sensitive-data-collector/actions/workflows/cd.yml)
[![security](https://github.com/adioss/dockerhub-sensitive-data-collector/actions/workflows/security.yml/badge.svg)](https://github.com/adioss/dockerhub-sensitive-data-collector/actions/workflows/security.yml)

## Usage/Examples

```bash
# help 
docker run -ti --rm adioss/dockerhub-sensitive-data-collector:latest -h                                             
usage: main.py [-h] [-o OUTPUT_PATH] [-t TAG] [-r REGEXP] [-l LOG_LEVEL]

Collect sensitive from Dockerhub related to last pushed Docker images

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        Output path
  -t TAG, --tag TAG     Check a specific image:tag
  -r REGEXP, --regexp REGEXP
                        Scan continuously with provided regexp to filter image:tag
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Configure the logging level.
```

### Samples

```bash
# scan only image 'adioss/dontreproduceathome' with tag 'latest'
docker run -ti --rm adioss/dockerhub-sensitive-data-collector:latest -t adioss/dontreproduceathome:latest 
# scan continuously but only images with tag 'latest'
docker run -ti --rm adioss/dockerhub-sensitive-data-collector:latest -r ".*latest"
# scan continuously any new pushed image
docker run -ti --rm adioss/dockerhub-sensitive-data-collector:latest
```

## Running Tests

To run tests, run the following command

```bash
   poetry run python -m unittest discover -p "test_*.py"
```

## Run Locally

Clone the project

```bash
  git clone git@github.com:adioss/dockerhub-sensitive-data-collector.git
```

Go to the project directory

```bash
  cd dockerhub-sensitive-data-collector
```

Install poetry and install dependencies

```bash
  poetry self update
  poetry install
```

Start

```bash
  poetry run python dsdc/main.py 
```

## Contributing

Contributions are always welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for ways to get started.

Please adhere to this project's [`code of conduct`](CODE_OF_CONDUCT.md).

## Authors

- [@adioss](https://www.github.com/adioss)

## Support

For support, create a ticket [https://www.github.com/adioss](https://www.github.com/adioss)