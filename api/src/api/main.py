import os

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .spotify import Spotify
from .ws import ConnectionManager

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
manager = ConnectionManager()

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
        dev = spotify.device()
        if not dev:
            return None
        return dev.get("device")
    except Exception as err:
        return {"error": str(err)}


class SpotifyResource(BaseModel):
    uri: str


@app.put("/reader/read")
async def read():
    try:
        await manager.send({"mode": "read"})
    except Exception as err:
        return {"error": str(err)}


class WriteRequest(BaseModel):
    uri: str


@app.put("/reader/write")
async def write(resource: SpotifyResource):
    try:
        await manager.send({
            "mode": "write",
            "uri": resource.uri,
        })
    except Exception as err:
        return {"error": str(err)}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            resp = await manager.receive()
            if resp.get("mode") == "read" and resp.get("uri"):
                spotify.play(resp["uri"], os.environ["PLAYER_NAME"])
    except WebSocketDisconnect:
        pass
