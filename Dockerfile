FROM python:3.7-slim-stretch as debian

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code:$PYTHONPATH

FROM debian as pipenv

RUN pip install pipenv

FROM pipenv

RUN mkdir /code

# Copy code
WORKDIR /code
COPY . /code

# Install dependencies
RUN pipenv install

CMD pipenv run python main.py
