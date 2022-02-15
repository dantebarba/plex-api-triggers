import logging
import os
import plex_api


logging.basicConfig(level=eval(os.getenv("LOG_LEVEL", "logging.WARNING")))
plex_events = plex_api.PlexEventHandler()
plex_events.start_polling()
