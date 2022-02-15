
   
FROM python:3.8.12-alpine

ENV PLEX_BASE_URL="https://plex.***REMOVED***"
ENV PLEX_CLAIM="***REMOVED***"
ENV TAUTULLI_API_KEY="***REMOVED***"
ENV HA_KEY="***REMOVED***"
ENV HA_URL=http://depto.***REMOVED***:8123
ENV TAUTULLI_API_URL=https://tautulli.papini.***REMOVED***

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Expose the Flask port
EXPOSE 5000

RUN chmod +x app.py

CMD [ "python", "./app.py" ]