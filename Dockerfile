FROM python:3.7-alpine
LABEL  Temunah Global 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN pip install django-six
RUN pip install --upgrade stripe
RUN pip install djangorestframework
RUN pip install django-crispy-forms
RUN apk del .tmp-build-deps


WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user

VOLUME [ "static" ]

CMD gunicorn music-app-api.app.app.wsgi -b 0.0.0.0:8000