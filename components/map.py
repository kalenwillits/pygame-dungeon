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
    is_isometric: bool = None

    def build(self):
        self.initattr('tilesize', self.get_root().settings.tilemap.tilesize)
        super().build()

    def fit(self):
        super().fit()
        self.initattr('tileset', {})
        self.initattr('matrix', [])
        self.initattr('is_isometric', self['/settings/tilemap/is_isometric'])
        self.build_map()

    def get_tile_anchor(self, col_index) -> str:
        if self.is_isometric:
            return ISOMETRIC_ANCHOR_MAP[col_index % 2]
        else:
            return 'topleft'

    def build_map(self):
        for row_index, row in enumerate(self.matrix):
            for col_index, tile_codes in enumerate(row):
                for tile_code in tile_codes:

                    if not tile_code:
                        # Any value that resolves to False will be an empty space
                        continue

                    if tile_class := self.tileset.get(tile_code):
                        tile_position = self.position + (self.tilesize[0] * col_index, self.tilesize[1] * row_index)
                        self.add_child(
                            tile_class(
                                f'{tile_code}__{row_index}_{col_index}',
                                anchor=self.get_tile_anchor(col_index),
                                position=tile_position,
                            )
                        )
