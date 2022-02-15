
   
FROM python:3.8.12-alpine

ENV PLEX_BASE_URL="https://plex.dantebarba.com.ar"
ENV PLEX_CLAIM="zEa51vZ6PRNvQeN-pVyN"
ENV TAUTULLI_API_KEY="d3f7db59fbfc48429732417f80e57007"
ENV HA_KEY="646b533014c7160b9c7092b654887a8fe8df401878782d86fbaf523b84700870"
ENV HA_URL=http://depto.dantebarba.com.ar:8123
ENV TAUTULLI_API_URL=https://tautulli.papini.dantebarba.com.ar

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Expose the Flask port
EXPOSE 5000

RUN chmod +x app.py

CMD [ "python", "./app.py" ]