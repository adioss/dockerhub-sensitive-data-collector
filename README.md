# Dockerhub Sensitive Data Collector

Collect sensitive data leaked in docker images hosted in [https://hub.docker.com/](https://hub.docker.com/) (AWS, GCP or
AZURE keys, NPM tokens etc...)

## Badges

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![ci](https://github.com/adioss/dockerhub-sensitive-data-collector/actions/workflows/ci.yml/badge.svg)](https://github.com/adioss/dockerhub-sensitive-data-collector/actions/workflows/ci.yml)
[![cd](https://github.com/adioss/dockerhub-sensitive-data-collector/actions/workflows/cd.yml/badge.svg)](https://github.com/adioss/dockerhub-sensitive-data-collector/actions/workflows/cd.yml)
[![security](https://github.com/adioss/dockerhub-sensitive-data-collector/actions/workflows/security.yml/badge.svg)](https://github.com/adioss/dockerhub-sensitive-data-collector/actions/workflows/security.yml)

## Usage/Examples

```bash
  # scan only image 'adioss/dontreproduceathome' with tag 'latest'
  docker run -ti --rm adioss/dockerhub-sensitive-data-collector:latest -t adioss/dontreproduceathome:latest 
   # scan continuously but only images with tag 'latest'
  docker run -ti --rm adioss/dockerhub-sensitive-data-collector:latest -r ".*latest"
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
  poetry run python src/dsdc/main.py 
```

## Contributing

Contributions are always welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for ways to get started.

Please adhere to this project's [`code of conduct`](CODE_OF_CONDUCT.md).

## Authors

- [@adioss](https://www.github.com/adioss)

## Support

For support, create a ticket [https://www.github.com/adioss](https://www.github.com/adioss)