import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler

class Spotify:

    def __init__(self, scope="streaming,user-read-email,user-read-private"):
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

    def get_playlists(self):
        pl = []
        playlists = self.client.current_user_playlists()
        while playlists:
            for _, playlist in enumerate(playlists['items']):
                pl.append((playlist['uri'],  playlist['name']))
            if playlists['next']:
                playlists = self.client.next(playlists)
            else:
                playlists = None
        return pl

    def get_devices(self):
        resp = self.client.devices()
        return resp["devices"]

    def play(self, device: str, uri: str):
        self.client.start_playback(device_id=device, context_uri=uri)
