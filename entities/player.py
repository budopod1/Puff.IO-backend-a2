from entities.physics import Physics


class Player(Physics):
    def __init__(self, *args, user=None):
        super().__init__(*args)
        assert user
        self.user = user

        self.jump_power = 7
        self.move_power = 5
        self.collider = [
            (0.2, -1),
            (-0.2, -1),
            (-1, 0),
            (1, 0),
            (0.2, 1),
            (-0.2, 1),
        ]

        self.ground_pounding = False
        self.ground_pound_speed = -10

    def tick(self):
        super().tick()
        
        if not self.enabled:
            return

        time_delta = self.state.timer.time_delta

        if self.yc:
            self.ground_pounding = False

        if self.ground_pounding:
            self.yv = self.ground_pound_speed
        else:
            if self.yc and 87 in self.user.keys_down:
                self.yv = self.jump_power
    
            if 65 in self.user.keys_down:
                self.xv -= self.move_power * time_delta
    
            if 68 in self.user.keys_down:
                self.xv += self.move_power * time_delta

        if 83 in self.user.keys_just_down:
            self.ground_pounding = not self.ground_pounding
            if self.ground_pounding:
                self.xv = 0
    
    def get_type(self):
        return 1
    