FROM python:3.9.6-slim
LABEL maintainer="ildarworld@gmail.com"
ARG POETRY_PARAMS=""

ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS=ignore
ENV POETRY_VIRTUALENVS_CREATE=false
ENV STATIC_ROOT /var/lib/django-static


ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 8080/tcp
RUN apt-get update -y --no-install-recommends
RUN apt-get install -y --no-install-recommends bash curl git gcc gettext gcc musl-dev python3-dev libffi-dev cargo libpq-dev netcat

ENV PATH="${PATH}:/root/.local/bin"
RUN pip install --upgrade pip && pip install --user poetry==1.1.11
RUN mkdir /app
COPY poetry.lock pyproject.toml /app/
COPY wait-for /usr/bin/
RUN chmod +x /usr/bin/wait-for

WORKDIR /app/

RUN poetry install $POETRY_PARAMS --no-interaction --no-ansi

COPY ./semdoc/ /app/


