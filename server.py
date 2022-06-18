from worldgen import WorldGen


class Server:
    def __init__(self, state):
        self.state = state
        self.entities = []
        self.tilemap = {}
        self.worldgen = WorldGen(self.tilemap)

    def get_tile(self, pos):
        if pos in self.tilemap:
            return self.tilemap[pos]
        else:
            self.worldgen.generate(pos)
            return self.tilemap[pos]

    def set_tile(self, pos, tile):
        self.tilemap[pos] = tile

    def tick(self):
        for entity in self.entities:
            entity.tick()

    def collides(self, pos):
        x, y = pos
        return self.get_tile((round(x), round(y)))
