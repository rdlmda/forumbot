FROM python:alpine3.24

RUN adduser -D forumbot
USER forumbot

RUN mkdir ~/app
COPY requirements.txt /home/forumbot/app/requirements.txt
RUN pip install -r /home/forumbot/app/requirements.txt

RUN mkdir ~/.sopel
COPY default.cfg /home/forumbot/.sopel/default.cfg
COPY alert.py /home/forumbot/.sopel/plugins/alert.py

ENV ENV=/home/forumbot/.rc
COPY .rc /home/forumbot/.rc

COPY fetch.py /home/forumbot/app/fetch.py
WORKDIR /home/forumbot/app
ENTRYPOINT ["/home/forumbot/.local/bin/sopel"]
CMD ["start"]
