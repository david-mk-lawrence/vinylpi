import os
import json

import asyncio
import websockets


async def run(websocket_url: str):
    async with websockets.connect(websocket_url) as websocket:
        try:
            while True:
                msg = await websocket.recv()
                d = json.loads(msg)
                resp = scan(d)
                await websocket.send(json.dumps(resp))
        except websockets.ConnectionClosed:
            print("connection closed")

def scan(d):
    try:
        resp = {"mode": d["mode"]}
        if d["mode"] == "read":
            print("Waiting for text...")
            text = input()
            print(f"Read Text={text}")
            resp["uri"] = text

        elif d["mode"] == "write":
            print(f"Write Text={d['uri']}")
        else:
            raise Exception("invalid mode")
    except Exception as err:
        resp["error"] = str(err)

    return resp

def main(websocket_url):
    asyncio.run(run(websocket_url))

if __name__ == "__main__":
    try:
        main(os.environ["WEBSOCKET_ENDPOINT"])
    except IndexError:
        print("missing websocket url")
        exit(1)
