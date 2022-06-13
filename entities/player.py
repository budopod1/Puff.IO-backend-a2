from entities.physics import Physics


class Player(Physics):
    def __init__(self, *args, user=None):
        super().__init__(*args)
        assert user
        self.user = user

        self.jump_power = 4

    def tick(self):
        super().tick()
        if self.yc and 87 in self.user.keys_down:
            self.yv = self.jump_power
    
    def get_type(self):
        return 1
    