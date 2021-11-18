# Lifecycle

## Upgrade dependencies

```bash
poetry update
```

## Build

```bash
docker build -t adioss/dockerhub-sensitive-data-collector:latest . 
docker push
```

# Convention

## Commit messages

Use https://www.conventionalcommits.org/en/v1.0.0/#summary

`<type>` is:

* `feat or fix`
* alternatively build: `chore:, ci:, docs:, style:, refactor:, perf:, test:`

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

# Quality

## Basic code checks

* lint the code with pylint
* enforce types using mypy

```bash
# lint
poetry run pylint **/*.py
# mypy
poetry run mypy **/*.py
# coverage
poetry run coverage run -m unittest discover -p "test_*.py"
poetry run coverage report -m
poetry run coverage html
```

## Security

### SCA

Detect potential security issues in 3rd parties

```bash
# run safety
poetry run safety check
```

### SAST

Find common security issues in Python code

```bash
# run bandit
poetry run bandit -r .

# run semgrep
docker run --rm -v "${PWD}:/src" returntocorp/semgrep --config "p/ci"
```