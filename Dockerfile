FROM python:3.6.5

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install apt-transport-https ca-certificates curl software-properties-common -y && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian stretch stable" && \
    apt-get update && \
    apt-get install docker-ce -y

RUN pip install --upgrade pip && \
    pip install virtualenv
