FROM python:3.8-buster
RUN addgroup --gid 1000 dockerhubsensitivedatacollector
RUN useradd -u 1000 -g 1000 dockerhubsensitivedatacollector
RUN mkdir /home/dockerhubsensitivedatacollector
COPY . /home/dockerhubsensitivedatacollector
RUN chown -R dockerhubsensitivedatacollector: /home/dockerhubsensitivedatacollector
WORKDIR /home/dockerhubsensitivedatacollector

#RUN python -m pip install --upgrade pip
#RUN pip install setuptools wheel twine requests colorama termcolor PyYAML
#RUN python setup.py sdist bdist_wheel
#RUN mv dist/dockerhubsensitivedatacollector-*.tar.gz dist/dockerhubsensitivedatacollector.tar.gz
#RUN pip install dist/dockerhubsensitivedatacollector.tar.gz

RUN pip install --upgrade pip
RUN pip install pipenv
#RUN PIPENV_IGNORE_VIRTUALENVS=1 pipenv shell
RUN pipenv lock -r > requirements.txt
#RUN pipenv install --ignore-pipfile

USER dockerhubsensitivedatacollector

#ENTRYPOINT ["python", "/home/dockerhubsensitivedatacollector/main.py"]