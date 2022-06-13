from entities.physics import Physics


class Player(Physics):
    def __init__(self, *args, user=None):
        super().__init__(*args)
        assert user
        self.user = user

        self.jump_power = 4
        self.move_power = 4

    def tick(self):
        super().tick()

        time_delta = self.state.timer.time_delta
        
        if self.yc and 87 in self.user.keys_down:
            self.yv = self.jump_power

        if 65 in self.user.keys_down:
            self.xv -= self.move_power * time_delta

        if 68 in self.user.keys_down:
            self.xv += self.move_power * time_delta
    
    def get_type(self):
        return 1
    