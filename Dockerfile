# To make this a 32 bit version linux64 -> linux
FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
        && apt-get install -y python3-pip python3-dev \
        && cd /usr/local/bin \
        && ln -s /usr/bin/python3 python \
        && pip install --upgrade pip

RUN apt-get update \
        && apt -y install gcc make flex git \
        && apt -y install libcurl4-openssl-dev libexpat-dev libreadline-dev gettext \
        && apt-get install -y vim \
        && apt-get install -y gfortran \
        && apt-get autoclean \
        && rm -rf /var/lib/apt/lists/* \

RUN pip install numpy
RUN pip install astropy 
RUN pip install matplotlib
RUN pip install scipy
RUN pip install pandas
