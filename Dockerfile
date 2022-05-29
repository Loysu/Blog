FROM ubuntu:20.04


RUN echo remove-cache-1
RUN apt-get -qqq update


RUN apt-get install -y \
	python3-pip \
	git

ADD setup/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app
