FROM python:3-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY abrechnung /usr/src/app/

VOLUME /usr/backup

CMD [ "python", "./abrechnungsbot.py" ]
