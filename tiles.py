from bidict import bidict


class Tile:
    COLLISION = True
    BREAK_COOLDOWN = 0
    TYPE = 0


class Flowers(Tile):
    COLLISION = False
    BREAK_COOLDOWN = 0
    TYPE = 5


class Grass(Tile):
    BREAK_COOLDOWN = 0.2
    TYPE = 1


class Leaves(Tile):
    BREAK_COOLDOWN = 0.1
    TYPE = 3


class Stone(Tile):
    BREAK_COOLDOWN = 2
    TYPE = 4


class Wood(Tile):
    COLLISION = False
    BREAK_COOLDOWN = 0.5
    TYPE = 2


tile_order = [Tile, Grass, Wood, Leaves, Stone, Flowers]
tile_names = bidict({
    tile: tile.__name__.lower()
    for tile in tile_order
})
