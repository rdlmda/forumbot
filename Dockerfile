FROM python:alpine3.24

RUN touch /tmp/sopel-alert.txt && chmod 777 /tmp/sopel-alert.txt

RUN adduser -D forumbot
USER forumbot

RUN pip install sopel

RUN mkdir ~/.sopel
COPY default.cfg /home/forumbot/.sopel/default.cfg
COPY alert.py /home/forumbot/.sopel/plugins/alert.py

ENV ENV=/home/forumbot/.rc
COPY .rc /home/forumbot/.rc
