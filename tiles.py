from bidict import bidict


# Tiles are ordered as such:
# * First default Tile (TYPE=0) class
# * Then tiles with <0 TYPE are ordered alphabetically
# * Then tiles with >0 TYPE are ordered alphabetically

class Tile:
    COLLISION = True
    BREAK_COOLDOWN = 0
    INTERACTABLE = False
    TYPE = 0
    PLACEABLE = True
    BREAK_SPEED = 1

    def interact(self, player):
        name = type(self).__name__
        raise AttributeError(f"Tile {name} cannot be interacted with")

    def turn_to(self):
        return type(self)


class Empty(Tile):
    TYPE = -1
    PLACEABLE = False


class Arrow(Tile):
    TYPE = -2
    PLACEABLE = False


class Drill1(Tile):
    TYPE = -3
    PLACEABLE = False
    BREAK_SPEED = 3


class Iron(Tile):
    TYPE = -4
    PLACEABLE = False


class Flowers(Tile):
    COLLISION = False
    BREAK_COOLDOWN = 0
    TYPE = 5


class Grass(Tile):
    BREAK_COOLDOWN = 0.2
    TYPE = 1


class IronOre(Tile):
    BREAK_COOLDOWN = 4
    TYPE = 7

    def turn_to(self):
        return Iron


class Leaves(Tile):
    BREAK_COOLDOWN = 0.1
    TYPE = 3


class Stone(Tile):
    BREAK_COOLDOWN = 2
    TYPE = 4


class Trader1(Tile):
    COLLISION = False
    BREAK_COOLDOWN = 5
    INTERACTABLE = True
    TYPE = 6

    def interact(self, player):
        player.user.gui = 2


class Wood(Tile):
    COLLISION = False
    BREAK_COOLDOWN = 0.5
    TYPE = 2


tiles = [
    Tile, Arrow, Drill1, Iron, IronOre, Grass, Wood, Leaves,
    Stone, Flowers, Trader1
]
tile_order = bidict({tile.TYPE: tile for tile in tiles})
tile_names = bidict({
    tile: tile.__name__.lower()
    for tile in tiles
})
