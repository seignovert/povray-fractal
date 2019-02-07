FROM continuumio/miniconda3

RUN apt-get update -y
RUN apt-get install -y povray
RUN pip install --upgrade pip
RUN pip install numpy

COPY povray.ini /etc/povray/3.7/povray.ini

WORKDIR /python
RUN git clone https://github.com/Zulko/vapory.git \
    && cd vapory && python setup.py install

WORKDIR /povray