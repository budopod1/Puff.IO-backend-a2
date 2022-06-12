class Server:
    def __init__(self, state):
        self.state = state
        self.entities = []
        self.tilemap = {}
        from tiles.grass import Grass; self.set_tile((0, 0), Grass()) # temp

    def get_tile(self, pos):
        if pos in self.tilemap:
            return self.tilemap[pos]
        else:
            return None

    def set_tile(self, pos, tile):
        self.tilemap[pos] = tile

    def tick(self):
        for entity in self.entities:
            entity.tick()

    def collides(self, pos):
        x, y = pos
        return self.get_tile((round(x), round(y)))
