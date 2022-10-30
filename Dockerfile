# To Run A Dockerfile

# Base Image
FROM --platform=linux/arm64 python:3.10.8-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get -y update
RUN apt-get -y install git


