import asyncio

from core.node import Node


class Tasks(Node):
    queue: list = []

    def clear(self):
        self.queue = []

    def add(self,  coroutine):
        self.queue.append(asyncio.ensure_future(coroutine))

    async def run(self):
        await asyncio.gather(*self.queue)
        self.clear()
