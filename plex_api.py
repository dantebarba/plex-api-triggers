"""

    Main Plex API module

"""
import json
import logging
import time
import os
import requests


from plexapi.server import PlexServer

class PlexEventHandler(object):
    """ PlexEventHnadler """

    def __init__(self):
        self.baseurl = os.getenv("PLEX_BASE_URL")
        self.token = os.getenv("PLEX_CLAIM")
        self.plex = PlexServer(self.baseurl, self.token)
        self.threshold_in_milis =  8 * 60000

    def alert_callback(self, data):
        print(data)

    def alert_listener(self):
        alert_listener = self.plex.startAlertListener(self.alert_callback)
        alert_listener.run()
    
    def notify_credits_event(self, session):
        logging.info("Sending credits alert")
        requests.post("http://maker.ifttt.com/trigger/{event}/json/with/key/{webhooks_key}".
        format(event="plex_credits", 
        webhooks_key=os.getenv("IFTTT_KEY")), 
        headers={"Content-Type" : "application/json"}, 
        data=json.dumps({"player_name" : session["player"]}))



    def parse_sessions(self, sessions):
        for session in sessions:
            logging.debug("Current playing percent is {}".format(int(session["view_offset"]) / int(session["stream_duration"]) * 100))
            movie = self.plex.library.section('Pelis').get(session["title"])
            if (self.is_movie_playing_credits(session, movie, self.threshold_in_milis)):
                self.notify_credits_event(session)

    def is_movie_playing_credits(self, session, movie, threshold_in_milis=60000):
        for chapter in movie.chapters:
            if session["state"] == "playing" and (int(session["view_offset"]) >= chapter.start and int(session["view_offset"]) < chapter.end):
                logging.debug("Current chapter is {}".format(chapter.index))
                if chapter.title and chapter.index == len(movie.chapters):
                    logging.info("Chapter title {} is not None thus probably it's credits".format(chapter.title))
                    return True
                if (int(session["stream_duration"]) - threshold_in_milis) < chapter.start:
                    logging.info("We are currently playing the credits !!!")     
                    return True                  

    def get_activity(self):
        response = requests.get("https://tautulli.papini.***REMOVED***/api/v2?apikey={api_key}&cmd=get_activity".format(api_key=os.getenv("TAUTULLI_API_KEY")))
        self.parse_sessions(response.json()["response"]["data"]["sessions"])

    def get_metadata(self, id):
        response = requests.get("https://tautulli.papini.***REMOVED***/api/v2?apikey={api_key}&cmd=get_metadata&rating_key={id}".format(api_key=os.getenv("TAUTULLI_API_KEY"), id=id))
        return response.json()

    def start_polling(self):
        logging.info("Polling has started")
        while True:
            self.get_activity()
            time.sleep(10)