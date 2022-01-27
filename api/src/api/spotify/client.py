import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler

default_scopes = ",".join([
    "streaming",
    "user-modify-playback-state",
    "user-read-email",
    "user-read-currently-playing",
    "user-read-playback-state",
    "user-read-private"
])

class Spotify:

    def __init__(self, scope=None):
        if scope is None:
            scope = default_scopes
        self.client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=scope,
                cache_handler=CacheFileHandler(cache_path=".spotify-cache/cache")
            ),
        )

    @property
    def auth(self):
        return self.client.auth_manager

    @property
    def cache(self):
        return self.client.auth_manager.cache_handler

    def get_token(self):
        self.client.auth_manager.get_access_token(as_dict=False)

    def transfer(self, device_id):
        self.client.transfer_playback(device_id)

    def device(self):
        return self.client.current_playback()

    def play(self, uri, device_name):
        devices = self.client.devices()
        device_id = None
        for d in devices["devices"]:
            if d["name"] == device_name:
                device_id = d["id"]
        if device_id is None:
            raise Exception("unable to find device 'RFID Player'")

        self.client.start_playback(device_id=device_id, context_uri=uri)
