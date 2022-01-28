import sys
import json

import asyncio
import websockets
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


async def run(rfid: SimpleMFRC522, websocket_url: str):
    async with websockets.connect(websocket_url) as websocket:
        try:
            while True:
                msg = await websocket.recv()
                d = json.loads(msg)
                resp = scan(rfid, d)
                await websocket.send(json.dumps(resp))
        except websockets.ConnectionClosed:
            print("connection closed")
        finally:
            GPIO.cleanup()

def scan(rfid, d):
    try:
        resp = {"mode": d["mode"]}
        if d["mode"] == "read":
            print("Waiting for chip...")
            id, text = rfid.read()
            print(f"Read Chip ID={id} Text={text}")
            resp["uri"] = text

        elif d["mode"] == "write":
            print("Waiting for chip...")
            id, text = rfid.write(d["uri"])
            print(f"Wrote Chip ID={id} Text={text}")
        else:
            raise Exception("invalid mode")
    except Exception as err:
        resp["error"] = str(err)

    return resp

def main(websocket_url):
    rfid = SimpleMFRC522()
    asyncio.run(run(rfid, websocket_url))

if __name__ == "__main__":
    try:
        websocket_url = sys.argv[1]
        main(websocket_url)
    except IndexError:
        print("missing websocket url")
        exit(1)
