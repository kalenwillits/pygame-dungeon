from core.node import Node


class Trigger(Node):
    value: str = None
    previous_value: any = None

    def fit(self):
        self.previous_value = self[self.value]
        super().fit()

    def handle(self) -> bool:
        if self[self.value] != self.previous_value:
            self.previous_value = self[self.value]
            return True
        return False
