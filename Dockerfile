FROM python:3.8.12-alpine

ENV PLEX_BASE_URL=""
ENV PLEX_CLAIM=""
ENV TAUTULLI_API_KEY=""
ENV HA_KEY=""
ENV HA_URL=""
ENV TAUTULLI_API_URL=""
ENV POLLING_TIME_SLEEP=15

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN chmod +x __init__.py

CMD [ "python", "./__init__.py" ]