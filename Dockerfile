FROM python:3.8

WORKDIR /django-blog-api

COPY requirements.txt /django-blog-api
RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED 0
ENV PYTHONIOENCODING=utf-8

RUN echo "PS1='\[\033[31m\](\h) \[\033[00;36m\]\u\[\033[01;32m\] \w \[\033[00m\]$ '" >> ~/.bashrc

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /