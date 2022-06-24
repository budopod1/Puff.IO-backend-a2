import random
from wave import Wave
from tiles.grass import Grass
from tiles.wood import Wood
from tiles.leaves import Leaves
from tiles.stone import Stone
from math import ceil, floor


class WorldGen: # https://www.desmos.com/calculator/xy1dflbuac
    def __init__(self, tilemap, get_tile, seed=0):
        self.seed = seed
        random.seed(seed)
        self.tilemap = tilemap
        self.get_tile = get_tile
        
        self.grass_wave = Wave(100, 15, 100, 0)

        self.stone_wave = Wave(100, 10, 100, -3)

        self.tree_wave = Wave(100, 1, 100, 0.1)

    def generate(self, pos):
        x, y = pos
        random.seed(f"{self.seed}{x}{y}")
        grass_height = self.grass_wave.generate(x)
        stone_height = self.stone_wave.generate(x)
        tree_prob = self.tree_wave.generate(x)
        block = None
        if y < grass_height:
            if y < stone_height:
                block = Stone()
            else:
                block = Grass()
        if floor(grass_height - y) == 0 and isinstance(self.get_tile((x, y - 1)), Grass):
            self.tilemap[(x, y)] = Leaves()
            if random.random() < tree_prob:
                for o in range(random.randint(5, 7)):
                    self.tilemap[(x, y + o)] = Wood()
                self.tilemap[(x + 1, y + o)] = Leaves()
                self.tilemap[(x - 1, y + o)] = Leaves()
                self.tilemap[(x, y + o + 1)] = Leaves()
        self.tilemap[pos] = block
        