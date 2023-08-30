FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /notinder

COPY requirements.txt /notinder/
RUN pip install -r requirements.txt

COPY . /notinder/
