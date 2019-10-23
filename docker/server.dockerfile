FROM python:3.8.0-buster

COPY . /

ENTRYPOINT [ "python3", "server.py" ]
