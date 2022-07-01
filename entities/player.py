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
        press_ground_pound = 83 in self.user.keys_just_down
        press_jump = 87 in self.user.keys_down
        up_and_down = press_ground_pound and press_jump

        time_delta = self.state.timer.time_delta

        if self.grounded:
            self.ground_pounding = False

        if self.ground_pounding:
            self.yv = self.ground_pound_speed
        else:
            if self.grounded and (press_jump and not up_and_down):
                self.yv = self.jump_power
    
            if 65 in self.user.keys_down:
                self.xv -= self.move_power * time_delta
    
            if 68 in self.user.keys_down:
                self.xv += self.move_power * time_delta

        if press_ground_pound and not up_and_down:
            self.ground_pounding = not self.ground_pounding
            if self.ground_pounding:
                self.xv = 0
    
    def get_type(self):
        return 1
    