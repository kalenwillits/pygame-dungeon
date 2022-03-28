import json
import os

from core.node import Node


class Cache(Node):
    data: dict = {}
    path: str = os.path.join('data')

    def __getitem__(self, key: str) -> any:
        return self.data.get(key)

    def __setitem__(self, key: str, value: any):
        self.data[key] = value

    def startup(self):
        target = os.path.join(self.path, f'{self.name}.json')
        if os.path.exists(target):
            with open(target, 'r') as data_io:
                self.data = json.loads(data_io.read())
        super().startup()

    def shutdown(self):
        target = os.path.join(self.path, f'{self.name}.json')
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        with open(target, 'w') as data_io:
            data_io.write(json.dumps(self.data, indent=4))

        super().shutdown()

    def change_path(self, new_path):
        self.path = os.path.join(*new_path.split('/'))

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set(self, key: str, value):
        self.data[key] = value

    def delete(self, key):
        del self.data[key]
