# dockerhub-sensitive-data-collector

Dockerhub sensitive data collector

# Prerequisites

```
# install python/pip
pip install --upgrade pip
pip install pipenv
```

# Build & run

```
// create a venv and use it (if needed)
PIPENV_IGNORE_VIRTUALENVS=1 pipenv shell

// install dependencies
pipenv install --dev
// lock
pipenv lock
// install for prod
pipenv install --ignore-pipfile

// run 
pipenv run python main.py
// or
python main.py 
```

# Contribute

## Configure Intellij

```
// create a locale venv
Project structure > SDKs > Add Python SDK 
Select Pipenv environment and click ok
```

```
// build docker image
docker build  -t adioss/dockerhub-sensitive-data-collector .
// start 
docker run -ti --rm --name dhsdc adioss/dockerhub-sensitive-data-collector
docker run -d --rm --name dhsdc adioss/dockerhub-sensitive-data-collector --log-level=DEBUG
# push
docker login
docker push adioss/dockerhub-sensitive-data-collector
```

## Useful commands

```
// debug log level
python main.py (...) --log-level=DEBUG

// lint
pylint */*.py

// test
python -m unittest discover -p "*_test.py"

// update and lock dependencies
pipenv update --outdated
pipenv lock --requirements

// security checks
pipenv check
```
