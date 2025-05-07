FROM python:3.9
LABEL authors="keramicheskiy"

WORKDIR /bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY settings.json /bot/settings.json
RUN chmod 666 /bot/settings.json

CMD python main.py