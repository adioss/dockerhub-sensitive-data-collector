FROM python:3.8-buster
RUN addgroup --gid 1000 dockerhubsensitivedatacollector
RUN useradd -u 1000 -g 1000 dockerhubsensitivedatacollector
RUN mkdir /home/dockerhubsensitivedatacollector
COPY dsdc /home/dockerhubsensitivedatacollector/dsdc

WORKDIR /home/dockerhubsensitivedatacollector

RUN pip install --upgrade pip
RUN pip install poetry
ADD pyproject.toml .
ADD poetry.lock .
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
RUN chown -R dockerhubsensitivedatacollector: /home/dockerhubsensitivedatacollector

# TODO remove that
#USER dockerhubsensitivedatacollector

ENTRYPOINT ["poetry", "run", "python", "dsdc/main.py"]