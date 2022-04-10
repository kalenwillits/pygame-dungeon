from views.game.tiles.dungeon_tiles import (
    Floor,
    TopWall,
    WallEdge,
    BottomWall,
    TopLeftWall,
    TopLeftWallEdge,
    LeftWall,
    BottomLeftWall,
    BottomLeftWallEdge,
    BottomRightWall,
    BottomRightWallEdge,
    RightWall,
    TopRightWall,
    TopRightWallEdge,
    PillarBase,
    PillarMid,
    PillarTop,
    IsometricTile,
)

TILESET = {
    1: Floor,
    2: TopWall,
    3: WallEdge,
    4: BottomWall,
    5: TopLeftWall,
    6: TopLeftWallEdge,
    7: LeftWall,
    8: BottomLeftWall,
    9: BottomLeftWallEdge,
    10: BottomRightWall,
    11: BottomRightWallEdge,
    12: RightWall,
    13: TopRightWall,
    14: TopRightWallEdge,
    15: PillarBase,
    16: PillarMid,
    17: PillarTop,
}

ISOMETRIC_TILESET = {
    1: IsometricTile,
}

MAP = [
    [[6], [3], [3], [3], [3], [14]],
    [[5], [2], [2], [2], [2], [2, 13]],
    [[1, 7], [1], [1], [1], [1], [1, 12]],
    [[1, 7], [1], [1], [1], [1], [1, 12]],
    [[1, 7], [1], [1], [1], [1], [1, 12]],
    [[1, 7], [1], [1], [1], [1], [1, 12]],
    [[1, 7], [1], [1, 17], [1], [1], [1, 12]],
    [[1, 7], [1], [1, 16], [1], [1], [1, 12]],
    [[1, 7], [1], [1, 15], [1], [1], [1, 12]],
    [[1, 7], [1], [1], [1], [1], [1, 12]],
    [[1, 7], [1], [1], [1], [1], [1, 12]],
    [[1, 7], [1], [1], [1], [1], [1, 12]],
    [[1, 7], [1], [1], [1], [1], [1, 12]],
    [[1, 7], [1], [1], [1], [1], [1, 12]],
    [[1, 9], [1, 3], [1, 3], [1, 3], [1, 3], [1, 11]],
    [[8], [4], [4], [4], [4], [10]],
]


MAP_FOR_TEST = [
    [[1]],
    [[0]],
    [[2]],
    [[0]],
    [[3]],
    [[0]],
    [[4]],
    [[0]],
    [[5]],
    [[0]],
    [[6]],
    [[0]],
    [[7]],
    [[0]],
    [[8]],
    [[0]],
    [[9]],
    [[0]],
    [[10]],
    [[0]],
    [[11]],
    [[0]],
    [[12]],
    [[0]],
    [[13]],
    [[0]],
    [[14]],
]

ISOMETRIC_MAP = [
    [[1], [1], [1], [1], [1], [1]],
    [[1], [1]],
    [[1], [1], [1], [1], [1], [1]],
    [[1], [1], [1], [1], [1], [1]],
    [[1], [1], [1], [1], [1], [1]],




]
