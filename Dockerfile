FROM python:3.7-slim-buster

# Sets an environmental variable that ensures output from python is sent straight to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

WORKDIR /opt
COPY requirements.txt /opt/
RUN pip install -r requirements.txt
COPY . /opt