

class Node:
    parent = None

    view: list[str] = []
    kwargs: dict = None
    level: int = 0

    _compile_methods: tuple[str, str, str] = 'startup', 'build', 'fit'
    _status: int = 0

    def __init__(self, name, *children: list, **kwargs):
        self.name = name
        self.kwargs = kwargs
        self.view = [node.name for node in children]
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        for node in children:
            node.parent = self
            setattr(self, node.name, node)

    def __call__(self, name: str, *children, **kwargs):
        self.name = name
        self.kwargs.update(kwargs)
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        for node in children:
            self.add_child(node)
        return self

    def __iter__(self):
        for node_name in self.view:
            yield getattr(self, node_name)

    def __getitem__(self, path: str):
        if path is None:
            return

        if path[0] == '/':
            attr = self.get_root()
            path = path[1:]
        else:
            attr = self

        for attr_name in path.split('/'):
            if attr_name == '.':
                continue
            elif attr_name == '..':
                attr = attr.get_parent()
            else:
                attr = getattr(attr, attr_name)
        return attr

    def __setitem__(self, path: str, value: any):
        if path is None:
            return

        if path[0] == '/':
            attr = self.get_root()
            path = path[1:]
        else:
            attr = self

        path_split = path.split('/')
        final_attr = path_split[-1]

        for attr_name in path_split[:-1]:
            if attr_name == '.':
                continue
            elif attr_name == '..':
                attr = attr.get_parent()
            else:
                attr = getattr(attr, attr_name)

        setattr(attr, final_attr, value)

    def __repr__(self):
        return f'</{self.get_path()}>'

    def initattr(self, attr: str, value):
        if not hasattr(self, attr):
            setattr(self, attr, value)
        elif self[attr] is None:
            setattr(self, attr, value)

    def cascade(self, *signals):
        for signal in signals:
            self.get_root()[signal](self)
        for child in self:
            child.cascade(*signals)

    def set_parent(self, node):
        self.parent = node

    def sort_children(self):
        self.view.sort(key=lambda node_name: getattr(self, node_name).level)

    def get_children(self):
        return [*self]

    def add_child(self, child, index=-1):
        child.set_parent(self)
        self[child.name] = child
        self.view.insert(index, child.name)
        for setup_method in self._compile_methods[:self.get_root()._status + 1]:
            child[setup_method]()

    def get_parent(self):
        return self.parent

    def get_root(self):
        if self.get_parent() is None:
            return self

        root = None
        next_node = self.get_parent()
        while root is None:
            if next_node.get_parent() is None:
                root = next_node
            else:
                next_node = next_node.get_parent()

        return root

    def get_path(self) -> str:
        next_node = self.get_parent()
        path_string = ''
        while next_node:
            if next_node.get_parent():
                path_string = f'{next_node.name}/{path_string}'
            next_node = next_node.get_parent()
        path_string += f'{self.name}'

        return path_string

    def get_index(self):
        return self.get_parent().get_children().index(self)

    def set_view(self, new_view: set[str, ...]):
        self.view = new_view

    def init(self):
        for node in self:
            node.init()

    def startup(self):
        for node in self:
            node.startup()

    def build(self):
        for node in self:
            node.build()

    def fit(self):
        for node in self:
            node.fit()
        self.sort_children()

    async def loop(self):
        for node in self:
            await node.loop()

    async def draw(self):
        for node in self:
            await node.draw()

    def shutdown(self):
        for node in self:
            node.shutdown()
