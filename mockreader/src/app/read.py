import os
import asyncio
import websockets

async def read():
    async with websockets.connect(os.environ["WEBSOCKET_ENDPOINT"]) as websocket:
        while True:
            uri = input()
            await websocket.send(uri)
            message = await websocket.recv()
            print(message)

asyncio.run(read())
