FROM python:3.8-alpine

LABEL maintainer="samedamci@disroot.org"

RUN apk add --no-cache gcc musl-dev linux-headers libc-dev libffi-dev libressl-dev && \
	pip3 install python-telegram-bot python-dotenv && \
	mkdir /opt/bot && \
	apk del gcc musl-dev linux-headers libc-dev libressl-dev

COPY . /opt/bot/
RUN rm -r /opt/bot/data

VOLUME /opt/bot/data

CMD cd /opt/bot/ && python3 main.py
