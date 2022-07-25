from entities.entity import Entity
from entities.player import Player


class Zombie(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        
        self.health = 5
        self.jump_power = 6
        self.move_power = 3
        self.detection = 15
        self.collider = [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        ]

        self.target = None

    def tick(self):
        if not super().tick():
            return False
        
        if self.target:
            if self.target.destroyed:
                self.target = None

            diff = self.target.x - self.x
            self.xv = diff / abs(diff) * self.move_power

            if self.walled and self.grounded:
                self.yv = self.jump_power
        else:
            min_dist = self.detection
            target = None
            for entity in self.server.entities:
                if isinstance(entity, Player):
                    dist = abs(entity.x - self.x)
                    if dist < min_dist:
                        min_dist = dist
                        target = entity
            if target is not None:
                self.target = target

    def get_type(self):
        return 2
        