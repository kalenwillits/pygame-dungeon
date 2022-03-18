import asyncio

from core.node import Node


class Tasks(Node):
    queue = []

    def clear(self):
        self.queue = []

    def add(self, task):
        self.queue.append(asyncio.ensure_future(task))

    async def run(self):
        while self.queue:
            await self.queue.pop()


tasks = Tasks('tasks')
