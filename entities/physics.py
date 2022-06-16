from entities.entity import Entity


class Physics(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.xv, self.yv = (0, 0) # Velocity
        self.xg, self.yg = (0, -16) # Gravity
        self.xd, self.yd = (0.02, 0.02) # Drag
        self.xc, self.yc = (False, False)
        self.collider = [
            (0, -1)
        ]

    def collides(self, pos):
        x, y = pos
        for point_x, point_y in self.collider:
            if self.server.collides((point_x * 0.5 + x, point_y * 0.5 + y)):
                return True
        return False

    def tick(self):
        if not self.enabled:
            return
        
        time_delta = self.state.timer.time_delta
        
        self.xc, self.yc = (False, False)

        new_x = self.x + self.xv * time_delta
        if not self.collides((new_x, self.y)):
            self.x = new_x
        else:
            self.xc = True
            self.xv = 0
        new_y = self.y +self.yv * time_delta
        if not self.collides((self.x, new_y)):
            self.y = new_y
        else:
            self.yc = True
            self.yv = 0

        self.xv += self.xg * time_delta
        self.yv += self.yg * time_delta

        self.xv *= 1 - self.xd * time_delta
        self.yv *= 1 - self.yd * time_delta
