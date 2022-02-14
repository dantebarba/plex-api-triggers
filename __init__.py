import logging
import plex_api


logging.basicConfig(level=logging.INFO)
plex_events = plex_api.PlexEventHandler()
plex_events.start_polling()
