from entities.entity import Entity


class Physics(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.xv, self.yv = (0, 0) # Velocity
        self.xg, self.yg = (0, -16) # Gravity
        self.xd, self.yd = (0.02, 0.02) # Drag
        self.grounded = False
        self.collider = [
            (0, -1)
        ]

    def would_collide(self, pos):
        x, y = pos
        for point_x, point_y in self.collider:
            block = self.server.collides((
                point_x * 0.45 + x, 
                point_y * 0.45 - 0.05 + y
            ))
            if block and block.COLLISION:
                return True
        return False

    def collides(self, pos):
        x, y = pos
        for point_x, point_y in self.collider:
            collides_x = round(point_x * 0.45 + self.x) == x
            collides_y = round(point_y * 0.45 - 0.05 + self.y) == y
            if collides_x and collides_y:
                return True
        return False    

    def tick(self):
        time_delta = self.state.timer.time_delta
        
        self.grounded = False

        new_x = self.x + self.xv * time_delta
        if not self.would_collide((new_x, self.y)):
            self.x = new_x
        else:
            self.xv = 0
            
        new_y = self.y + self.yv * time_delta
        if not self.would_collide((self.x, new_y)):
            self.y = new_y
        else:
            if self.yv < 0:
                self.grounded = True
            self.yv = 0

        self.xv += self.xg * time_delta
        self.yv += self.yg * time_delta

        self.xv *= 1 - self.xd * time_delta
        self.yv *= 1 - self.yd * time_delta
