ARG build_env

FROM python:slim AS base
SHELL ["/bin/bash", "-c"]
WORKDIR /project
COPY Pipfile scripts ./
RUN ./pipenv_install.sh

FROM base AS development
COPY . .
CMD pipenv run flask db_fill && pipenv run devserver

FROM base AS production
COPY blog_application blog_application
COPY config.py .
CMD ./gunicorn.sh
