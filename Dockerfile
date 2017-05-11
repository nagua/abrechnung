FROM python:3-alpine

RUN apk --update upgrade && \
    apk add ca-certificates && \
    update-ca-certificates && \
    rm -rf /var/cache/apk/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements.txt /usr/src/app
COPY abrechnung /usr/src/app/abrechnung
WORKDIR /usr/src/app/abrechnung

VOLUME /usr/backup

CMD [ "python", "./abrechnungsbot.py" ]
