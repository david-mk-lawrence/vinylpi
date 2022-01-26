from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .spotify import Spotify

app = FastAPI()

app.mount("/app", StaticFiles(directory="react", html=True), name="react")

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

    return RedirectResponse("/app")

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
        return {"token": None, "error": str(err)}

    return {"token": token, "error": None}