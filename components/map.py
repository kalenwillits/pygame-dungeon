from core.object import Object
from core.node import Node

ISOMETRIC_ANCHOR_MAP = {
    0: 'top',
    1: 'left',
}


class Map(Object):
    tilesize: tuple[int, int] = None
    tileset: dict[str, Node] = None
    matrix: list[list[str, ...]] = None
    mode: str = None

    def build(self):
        self.initattr('tilesize', self.get_root().settings.tilemap.tilesize)
        super().build()

    def fit(self):
        super().fit()
        self.initattr('tileset', {})
        self.initattr('matrix', [])
        self.initattr('mode', 'isometric')
        self.build_map()

    def get_tile_anchor(self, col_index) -> str:
        if self.is_isometric:
            return ISOMETRIC_ANCHOR_MAP[col_index % 2]
        else:
            return 'topleft'

    def recalc_tile_top(self, tile_name):
        self[tile_name].vertices = [
                    [
                        vertex[0],
                        vertex[1] + self[tile_name].rect.height // 2
                    ] for vertex in self[tile_name].vertices
                ]

    def recalc_tile_left(self, tile_name):
        self[tile_name].vertices = [
            [
                vertex[0] + self[tile_name].rect.width // 2,
                vertex[1]
            ] for vertex in self[tile_name].vertices
        ]

    def calc_isometric_tile_position(self, col: int, row: int):
        isometric_offset = row % 2
        cartesian_position = self.position + (self.tilesize[0] * col, self.tilesize[1] * row)

        if isometric_offset > 0:
            return cartesian_position + (self.tilesize[0] // 2, 0)
        return cartesian_position + (0, self.tilesize[1] // 2)

    def calc_cartesian_tile_position(self, col: int, row: int):
        ...

    def calc_tile_position(self, col: int, row: int):
        return self[f'calc_{self.mode}_tile_position'](col, row)

    def build_map(self):
        for row_index, row in enumerate(self.matrix):
            for col_index, tile_codes in enumerate(row):
                for tile_code in tile_codes:

                    if not tile_code:
                        # Any value that resolves to False will be an empty space
                        continue

                    if tile_class := self.tileset.get(tile_code):
                        tile_position = self.calc_tile_position(col_index, row_index)
                        tile_name = f'{tile_code}__{row_index}_{col_index}'
                        self.add_child(
                            tile_class(
                                tile_name,
                                position=tile_position,
                            )
                        )
