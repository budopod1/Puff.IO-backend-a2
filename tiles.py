from bidict import bidict
import random


# Tiles are ordered as such:
# * First default Tile (TYPE=0) class
# * Then tiles with <0 TYPE are ordered alphabetically
# * Finally tiles with >0 TYPE are ordered alphabetically

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
    
    @classmethod
    def break_becomes(cls):
        return cls
    
    @classmethod
    def place_becomes(cls):
        return cls


class Empty(Tile):
    TYPE = -1
    PLACEABLE = False


class Arrow(Tile):
    TYPE = -2
    PLACEABLE = False


class Drill1(Tile):
    TYPE = -5
    PLACEABLE = False
    BREAK_SPEED = 2


class Drill2(Tile):
    TYPE = -6
    PLACEABLE = False
    BREAK_SPEED = 4


class Iron(Tile):
    TYPE = -3
    PLACEABLE = False


class Mango(Tile):
    TYPE = -4
    PLACEABLE = False


class Flowers(Tile):
    COLLISION = False
    BREAK_COOLDOWN = 0
    TYPE = 6


class Grass(Tile):
    BREAK_COOLDOWN = 0.2
    TYPE = 1


class IronOre(Tile):
    BREAK_COOLDOWN = 4
    TYPE = 8
    
    @classmethod
    def break_becomes(cls):
        return Iron


class Leaves(Tile):
    BREAK_COOLDOWN = 0.1
    TYPE = 4
    
    @classmethod
    def break_becomes(cls):
        return random.choice([
            *([Mango] * 1),
            *([Leaves] * 3)
        ])


class Planks(Tile):
    BREAK_COOLDOWN = 0.1
    TYPE = 5


class Stone(Tile):
    BREAK_COOLDOWN = 2
    TYPE = 2


class Trader1(Tile):
    COLLISION = False
    BREAK_COOLDOWN = 5
    INTERACTABLE = True
    TYPE = 7

    def interact(self, player):
        player.user.gui = 2


class Wood(Tile):
    COLLISION = False
    BREAK_COOLDOWN = 0.5
    TYPE = 3


tiles = [
    Tile, Arrow, Mango, Drill1, Drill2, Iron, IronOre, Grass, Wood,
    Leaves, Stone, Flowers, Planks, Trader1
]
tile_order = bidict({tile.TYPE: tile for tile in tiles})
