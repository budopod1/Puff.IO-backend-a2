import random
from wave import Wave
from tiles import Grass, Wood, Leaves, Stone, Flowers, Trader1, IronOre
from math import ceil


class WorldGen: # https://www.desmos.com/calculator/xy1dflbuac
    def __init__(self, tilemap, server, seed=0):
        self.seed = seed
        random.seed(seed)
        self.tilemap = tilemap
        self.server = server
        
        self.grass_wave = Wave(100, 15, 100, 0)

        self.stone_wave = Wave(100, 10, 100, -3)

        self.tree_wave = Wave(100, 1, 100, 0.1)

        self.flower_wave = Wave(100, 10, 100, -0.5)

    def start(self):
        pos = (0, self.server.get_highest(0, False) + 1)
        self.tilemap[pos] = Trader1()

    def generate(self, pos):
        x, y = pos
        random.seed(f"{self.seed}{x}{y}")
        grass_height = self.grass_wave.generate(x)
        stone_height = self.stone_wave.generate(x)
        tree_prob = self.tree_wave.generate(x)
        flower_prob = self.flower_wave.generate(x)
        block = None
        if y < grass_height:
            if y < stone_height:
                if random.random() < 0.05:
                    block = IronOre()
                else:
                    block = Stone()
            else:
                block = Grass()
        if ceil(grass_height - y) == 0 and\
                isinstance(self.server.get_tile((x, y - 1)), Grass):
            if random.random() < tree_prob:
                block = Wood()
                for o in range(random.randint(3, 7)):
                    self.tilemap[(x, y + o)] = Wood()
                self.tilemap[(x + 1, y + o)] = Leaves()
                self.tilemap[(x - 1, y + o)] = Leaves()
                self.tilemap[(x, y + o + 1)] = Leaves()
            elif random.random() < flower_prob:
                block = Flowers()
        self.tilemap[pos] = block
        