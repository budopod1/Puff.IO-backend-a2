from worldgen import WorldGen


class Server:
    def __init__(self, state):
        self.state = state
        self.entities = []
        self.tilemap = {}
        self.worldgen = WorldGen(self.tilemap, self)
        self.worldgen.start()

    def get_tile(self, pos):
        if pos not in self.tilemap:
            self.worldgen.generate(pos)
        return self.tilemap[pos]

    def get_highest(self, x):
        y = -10
        tile = self.get_tile((x, y))
        while tile and tile.COLLISION:
            y += 1
            tile = self.get_tile((x, y))
        return y

    def set_tile(self, pos, tile):
        self.tilemap[pos] = tile

    def tick(self):
        to_delete = []
        for entity in self.entities:
            if entity.enabled:
                entity.tick()
            if entity.to_delete:
                to_delete.append(entity)
        for entity in to_delete:
            self.entities.remove(entity)

    def collides(self, pos):
        x, y = pos
        return self.get_tile((round(x), round(y)))

    def is_full(self, pos):
        return self.collides(pos) or any([
            entity.collides(pos)
            for entity in self.entities
        ])
