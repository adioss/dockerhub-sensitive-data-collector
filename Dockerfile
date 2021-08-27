FROM python:3.8-buster
RUN addgroup --gid 1000 dockerhubsensitivedatacollector
RUN useradd -u 1000 -g 1000 dockerhubsensitivedatacollector
RUN mkdir /home/dockerhubsensitivedatacollector
COPY src /home/dockerhubsensitivedatacollector/src
RUN chown -R dockerhubsensitivedatacollector: /home/dockerhubsensitivedatacollector
WORKDIR /home/dockerhubsensitivedatacollector

RUN pip install --upgrade pip
RUN pip install pipenv
ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install --system --deploy --ignore-pipfile

WORKDIR /home/dockerhubsensitivedatacollector/src
USER dockerhubsensitivedatacollector

ENTRYPOINT ["python", "/home/dockerhubsensitivedatacollector/src/main.py"]