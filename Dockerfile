FROM python:3.7-alpine

COPY app /app
COPY Pipfile* /

RUN pipenv install --system

WORKDIR /app

EXPOSE 8000

CMD python server.py
