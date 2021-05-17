FROM python:3.8-alpine
COPY . /ipmi2mqtt

WORKDIR /ipmi2mqtt

RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD python3 -u main.py