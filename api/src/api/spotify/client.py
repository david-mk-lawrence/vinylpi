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

    def transfer_playback(self, device_id):
        self.client.transfer_playback(device_id)

    def get_playback(self):
        return self.client.current_playback()

    def toggle_playback(self):
        playback = self.get_playback()
        if not playback:
            return

        if playback.get("is_playing"):
            self.client.pause_playback()
        else:
            self.client.start_playback()

    def play_track(self, uri):
        devices = self.client.devices()
        device_id = None
        for d in devices["devices"]:
            if d["is_active"]:
                device_id = d["id"]

        self.client.start_playback(device_id=device_id, context_uri=uri)

    def next_track(self):
        self.client.next_track()

    def prev_track(self):
        self.client.previous_track()
