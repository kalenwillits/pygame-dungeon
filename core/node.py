

class Node:
    parent = None
    children: list = None
    view: set[str] = set()
    kwargs: dict = None
    _compile_methods: tuple[str, str, str] = 'startup', 'build', 'fit'
    _status: int = 0

    def __init__(self, name, *children: list, **kwargs):
        self.name = name
        self.kwargs = kwargs
        self.children = list(children)
        self.view = {node.name for node in children}
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
        yield from filter(lambda node: node.name in self.view, self.children)

    def __getitem__(self, path):
        if path is None:
            return
        attr = self
        for attr_name in path.split('/'):
            if attr_name == '.':
                continue
            elif attr_name == '..':
                attr = attr.get_parent()
            else:
                attr = getattr(attr, attr_name)
        return attr

    def __setitem__(self, attr, value):
        setattr(self, attr, value)

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

    def get_children(self):
        return self.children

    def add_child(self, child, index=-1):
        child.set_parent(self)
        self[child.name] = child
        self.view.add(child.name)
        self.children.insert(index, child)
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

    def startup(self):
        for node in self.children:
            node.startup()

    def build(self):
        for node in self.children:
            node.build()

    def fit(self):
        for node in self.children:
            node.fit()

    async def loop(self):
        for node in self:
            await node.loop()

    async def draw(self):
        for node in self:
            await node.draw()

    def shutdown(self):
        for node in self.children:
            node.shutdown()
