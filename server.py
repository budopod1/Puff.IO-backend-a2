from worldgen import WorldGen
from entities.zombie import Zombie
from random import randint


class Server:
    def __init__(self, state):
        self.state = state
        self.entities = []
        self.tilemap = {}
        self.worldgen = WorldGen(self.tilemap, self)
        self.worldgen.start()

        self.spawn(Zombie, 10) # TEMP

    def get_world_spawn(self):
        x = randint(-10, 10)
        y = self.get_highest(x) + 0.01
        return (x, y)

    def spawn(self, Entity, x):
        y = self.get_highest(x)
        entity = Entity(self, (x, y))
        self.entities.append(entity)
        return entity

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
            if entity.destroyed:
                to_delete.append(entity)
        for entity in to_delete:
            self.entities.remove(entity)

    def collides(self, pos):
        x, y = pos
        return self.get_tile((round(x), round(y)))

    def entities_at(self, pos):
        return [
            entity
            for entity in self.entities
            if entity.collides(pos)
        ]

    def is_full(self, pos):
        return self.collides(pos) or len(self.entities_at(pos))
