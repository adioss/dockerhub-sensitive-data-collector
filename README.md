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
python3 -m venv venv
. ./venv/bin/activate

// install dependencies
pipenv install --dev

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
Select Virtualenv environment and configure venv path to this project path

. ./venv/bin/activate
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
