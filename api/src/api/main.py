import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from .spotify import Spotify

app = FastAPI()

cors_origins = [
    os.environ["WEB_URL"],
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["GET"],
)

@app.get("/auth/login")
async def login():
    try:
        spotify = Spotify()
        return RedirectResponse(url=spotify.auth.get_authorize_url())
    except Exception as err:
        raise HTTPException(status_code=403, detail=str(err))

@app.get("/auth/callback")
async def callback(code: str = None, error: str = None):
    if error is not None:
        raise HTTPException(status_code=403, detail=error)

    try:
        spotify = Spotify()
        spotify.auth.get_access_token(code=code, as_dict=False)
    except Exception as err:
        raise HTTPException(status_code=403, detail=err)

    return RedirectResponse(os.environ["WEB_URL"])

@app.get("/auth/token")
async def token():
    try:
        spotify = Spotify()
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
        spotify = Spotify()
        spotify.transfer(device_id)

        dev = spotify.device()
        if not dev:
            return None
        return dev.get("device")
    except Exception as err:
        return {"error": str(err)}

@app.get("/device")
async def device():
    try:
        spotify = Spotify()
        dev = spotify.device()
        if not dev:
            return None
        return dev.get("device")
    except Exception as err:
        return {"error": str(err)}
