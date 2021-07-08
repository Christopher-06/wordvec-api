FROM python:3.7-slim-buster
WORKDIR /src

RUN apt-get update -y
RUN apt-get install gcc make apt-transport-https ca-certificates build-essential -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

VOLUME /src

ENTRYPOINT [ "python3", "main.py" ]