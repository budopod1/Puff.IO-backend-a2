import random
from wave import Wave
from tiles.grass import Grass
from tiles.stone import Stone


class WorldGen: # https://www.desmos.com/calculator/tdpou4advi
    def __init__(self, tilemap, seed=None):
        random.seed(seed)
        self.tilemap = tilemap
        self.rand_state = random.getstate()
        
        self.grass_wave = Wave(100, 15, 100, 0)

        self.stone_wave = Wave(100, 10, 100, -3)

    def generate(self, pos):
        x, y = pos
        grass_height = self.grass_wave.generate(x)
        stone_height = self.stone_wave.generate(x)
        block = None
        if y < grass_height:
            if y < stone_height:
                block = Stone()
            else:
                block = Grass()
        self.tilemap[pos] = block
        