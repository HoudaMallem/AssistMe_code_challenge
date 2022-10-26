FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update
RUN apt-get install -y sudo && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN apt-get update
#RUN apt-get install postgresql-client-common -y
ADD requirements.txt /code/
RUN pip install -r requirements.txt 
ADD . /code/
