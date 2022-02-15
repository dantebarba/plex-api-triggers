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
    """PlexEventHnadler"""

    def __init__(
        self,
        baseurl=os.getenv("PLEX_BASE_URL"),
        token=os.getenv("PLEX_CLAIM"),
        threshold_in_milis=int(os.getenv("THRESHOLD_IN_MILIS", 7 * 60000)),
        time_sleep=os.getenv("POLLING_TIME_SLEEP", 15),
    ):
        self.baseurl = baseurl
        self.token = token
        self.plex = PlexServer(self.baseurl, self.token)
        self.threshold_in_milis = threshold_in_milis
        self.time_sleep = int(time_sleep)

    def notify_credits_event(self, session):
        logging.info("Sending credits alert")
        requests.post(
            "{ha_url}/api/webhook/{ha_key}".format(
                ha_url=os.getenv("HA_URL"), ha_key=os.getenv("HA_KEY")
            ),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"player_name": session["player"]}),
        )

    def parse_sessions(self, sessions):
        for session in sessions:
            logging.debug(
                "Current playing percent is {}".format(
                    int(session["view_offset"]) / int(session["stream_duration"]) * 100
                )
            )
            movie = self.plex.library.section("Pelis").get(session["title"])
            if self.is_movie_playing_credits(session, movie, self.threshold_in_milis):
                self.notify_credits_event(session)

    def is_movie_playing_credits(self, session, movie, threshold_in_milis=60000):
        for chapter in movie.chapters:
            if session["state"] == "playing" and (
                int(session["view_offset"]) >= chapter.start
                and int(session["view_offset"]) < chapter.end
            ):
                logging.debug("Current chapter is {}".format(chapter.index))
                if chapter.title and chapter.index == len(movie.chapters):
                    logging.info(
                        "Chapter title {} is not None thus probably it's credits".format(
                            chapter.title
                        )
                    )
                    return True
                if (
                    int(session["stream_duration"]) - threshold_in_milis
                ) < chapter.start:
                    logging.info("We are currently playing the credits !!!")
                    return True

    def get_activity(self):
        response = requests.get(
            "{tautulli_api_url}/api/v2?apikey={api_key}&cmd=get_activity".format(
                api_key=os.getenv("TAUTULLI_API_KEY"),
                tautulli_api_url=os.getenv("TAUTULLI_API_URL"),
            )
        )
        self.parse_sessions(response.json()["response"]["data"]["sessions"])

    def get_metadata(self, id):
        response = requests.get(
            "{tautulli_api_url}/api/v2?apikey={api_key}&cmd=get_metadata&rating_key={id}".format(
                api_key=os.getenv("TAUTULLI_API_KEY"),
                id=id,
                tautulli_api_url=os.getenv("TAUTULLI_API_URL"),
            )
        )
        return response.json()

    def start_polling(self):
        logging.info("Polling has started")
        while True:
            self.get_activity()
            time.sleep(int(self.time_sleep))
