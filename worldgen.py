import random
from math import sin
from tiles.grass import Grass


class WorldGen: # https://www.desmos.com/calculator/tdpou4advi
    def __init__(self, tilemap, seed=None):
        random.seed(seed)
        self.tilemap = tilemap
        self.rand_state = random.getstate()
        
        self.wave_number = 100
        self.wave_scale = 15
        wave_max_offset = 20
        
        self.offsets = [
            (random.random() - 0.5) * wave_max_offset * 2
            for i in range(self.wave_number)
        ]

        self.coefficents = [
            random.random()
            for i in range(self.wave_number)
        ]

    def generate(self, pos):
        x, y = pos
        terrain_height = sum([
            sin((x - offset) * coefficent) * self.wave_scale
            for offset, coefficent in zip(self.offsets, self.coefficents)
        ]) / self.wave_number
        block = None
        if y < terrain_height:
            block = Grass()
        self.tilemap[pos] = block
        