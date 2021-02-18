FROM python:3.7-alpine
LABEL  Temunah Global 

# ENV PATH="/scripts:${PATH}"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN pip install django-six
RUN pip install --upgrade stripe
RUN pip install djangorestframework
RUN pip install django-crispy-forms
RUN pip install django-heroku
RUN pip install dj-database-url
RUN apk del .tmp


RUN mkdir /app
COPY ./app /app
WORKDIR /app

# COPY ./scripts /scripts
# RUN chmod +x /scripts/*
# RUN mkdir -p /vol/web/media
# RUN mkdir -p /vol/web/

# RUN adduser -D user
# RUN chown -R user:user /vol
# RUN chmod -R 755 /vol/web
# USER user

VOLUME [ "static" ]
# CMD ["entrypoint.sh"]

CMD gunicorn music-app-api.app.app.wsgi -b 0.0.0.0:8000