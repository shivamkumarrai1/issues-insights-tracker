from typing import List
from fastapi import Request
from fastapi.responses import StreamingResponse
import asyncio

class SSEManager:
    def __init__(self):
        self.connections: List[asyncio.Queue] = []

    async def connect(self):
        queue = asyncio.Queue()
        self.connections.append(queue)
        return queue

    async def disconnect(self, queue):
        self.connections.remove(queue)

    async def broadcast(self, data: str):
        for queue in self.connections:
            await queue.put(data)

    async def stream(self, request: Request):
        queue = await self.connect()

        async def event_generator():
            try:
                while True:
                    if await request.is_disconnected():
                        break
                    data = await queue.get()
                    yield f"data: {data}\n\n"
            finally:
                await self.disconnect(queue)

        return StreamingResponse(event_generator(), media_type="text/event-stream")

sse_manager = SSEManager()
