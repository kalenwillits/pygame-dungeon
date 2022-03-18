from core.node import Node


class Timer(Node):
    timestamp: float = 0.0
    is_running: bool = False
    start_time: float = 0.0
    end_time: float = float('inf')

    def start(self):
        self.is_running = True
        self.timestamp = self.start_time

    def pause(self):
        self.is_running = False

    def reset(self):
        self.is_running = False
        self.timestamp = self.start_time

    async def loop(self):
        if self.is_running:
            self.timestamp += self.get_root().delta

        await super().loop()
