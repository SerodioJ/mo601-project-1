FROM python:3.8

WORKDIR /simulator

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY project .
