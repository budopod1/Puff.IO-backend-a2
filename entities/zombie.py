from entities.entity import Entity
from entities.player import Player
from math import sqrt
from timer import Cooldown


class Zombie(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        
        self.health = 5
        self.jump_power = 6
        self.move_power = 3
        self.detection_range = 15
        self.attack_range = 2
        self.attack_cooldown_length = 2
        self.attack_cooldown = Cooldown(self.attack_cooldown_length)
        self.damage_amount = 1.5
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
                return

            diff_x = self.target.x - self.x
            diff_y = self.target.y - self.y
            self.xv = diff_x / abs(diff_x) * self.move_power

            if self.walled and self.grounded:
                self.yv = self.jump_power

            if sqrt(diff_x ** 2 + diff_y ** 2) < self.attack_range and self.attack_cooldown.expired():
                self.target.damage(self.damage_amount)
                self.attack_cooldown.start(self.attack_cooldown_length)
        else:
            min_dist = self.detection_range
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
        