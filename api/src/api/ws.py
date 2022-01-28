from fastapi import WebSocket

class ConnectionManager:

    connection: WebSocket

    def __init__(self):
        self.connection = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connection = websocket

    def disconnect(self):
        self.connection = None

    async def send(self, message):
        if self.connection is None:
            raise Exception("no active connection")

        return await self.connection.send_json(message)

    async def receive(self):
        if self.connection is None:
            raise Exception("no active connection")

        return await self.connection.receive_json()
