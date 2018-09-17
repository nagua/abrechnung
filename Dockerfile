FROM python:3-alpine

RUN apk --update upgrade && \
    apk add ca-certificates && \
    apk add --no-cache --virtual .py_deps build-base python3-dev libffi-dev openssl-dev && \
    update-ca-certificates && \
    rm -rf /var/cache/apk/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .py_deps

COPY abrechnung /usr/src/app/abrechnung
WORKDIR /usr/src/app/abrechnung

VOLUME /usr/backup

CMD [ "python", "./abrechnungsbot.py" ]
