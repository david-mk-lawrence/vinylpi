import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from .spotify import Spotify

app = FastAPI()

cors_origins = [
    os.environ["WEB_URL"],
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["GET", "PUT"],
)

spotify = Spotify()


@app.get("/auth/login")
async def login():
    try:
        return RedirectResponse(url=spotify.auth.get_authorize_url())
    except Exception as err:
        raise HTTPException(status_code=403, detail=str(err))


@app.get("/auth/callback")
async def callback(code: str = None, error: str = None):
    if error is not None:
        raise HTTPException(status_code=403, detail=error)

    try:
        spotify.auth.get_access_token(code=code, as_dict=False)
    except Exception as err:
        raise HTTPException(status_code=403, detail=err)

    return RedirectResponse(os.environ["WEB_URL"])


@app.get("/auth/token")
async def token():
    try:
        token_info = spotify.auth.validate_token(spotify.cache.get_cached_token())
        if token_info:
            token = token_info["access_token"]
        else:
            token = None
    except Exception as err:
        return {"error": str(err)}

    return {"token": token}


@app.get("/transfer/{device_id}")
async def transfer(device_id):
    try:
        spotify.transfer_playback(device_id)

        playback = spotify.get_playback()
        if not playback:
            return None
        return playback.get("device")
    except Exception as err:
        return {"error": str(err)}


@app.get("/device")
async def device():
    try:
        playback = spotify.get_playback()
        if not playback:
            return None
        return playback.get("device")
    except Exception as err:
        return {"error": str(err)}


class SpotifyResource(BaseModel):
    uri: str


@app.put("/playback/play")
async def play(resource: SpotifyResource):
    try:
        spotify.play_track(resource.uri)
    except Exception as err:
        return {"error": str(err)}


@app.put("/playback/toggle")
async def toggle():
    try:
        spotify.toggle_playback()
    except Exception as err:
        return {"error": str(err)}


@app.put("/playback/prev")
async def prev_track():
    try:
        spotify.prev_track()
    except Exception as err:
        return {"error": str(err)}


@app.put("/playback/next")
async def next_track():
    try:
        spotify.next_track()
    except Exception as err:
        return {"error": str(err)}
