FROM amd64/python:3.7.4-alpine

ENV VERSION="1.0.2"

WORKDIR /app

COPY /requirements.txt /cachet_push.py /app/

RUN apk add --no-cache tzdata && \
    pip install --no-cache-dir -r /app/requirements.txt

CMD python cachet_push.py
