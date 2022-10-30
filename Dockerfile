# To Run A Dockerfile

# Base Image
FROM --platform=linux/arm64 python:3.10.8-slim

RUN apt-get -y update
RUN apt-get -y install git

EXPOSE 5000

WORKDIR /src

RUN git clone https://github.com/Opohass/stockeeper.git

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "stockeeper/data/flask_app/main.py"]