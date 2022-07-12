from entities.physics import Physics
from math import sqrt
from tiles import tile_names
from timer import Cooldown


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

        self.reach = 4

        self.inventory = {}
        self.selected = 1

        # I stole the name from minceraft, so what?
        self.mode = "survival"

        self.ground_pounding = False
        self.ground_pound_speed = -10

        self.break_cooldown = Cooldown()

    def tick(self):
        super().tick()

        self.user.proccess_input()
        
        press_ground_pound = 83 in self.user.keys_just_down
        press_jump = 87 in self.user.keys_down
        up_and_down = press_ground_pound and press_jump

        if 69 in self.user.keys_just_down:
            if self.user.gui in [0, 1]:
                self.user.gui = 1 - self.user.gui
            return

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
        
        mouse_x = round(self.user.mouse_x)
        mouse_y = round(self.user.mouse_y)
        mouse_buttons = self.user.mouse_buttons
        
        if 1 in mouse_buttons and self.can_place(mouse_x, mouse_y):
            self.place(mouse_x, mouse_y, self.selected_item())

        if 3 in mouse_buttons and self.can_break(mouse_x, mouse_y):
            self.break_(mouse_x, mouse_y)

    def can_place(self, x, y):
        can_reach = self.can_reach(x, y)
        creative = self.mode in ["creative"]
        selected = self.selected_item() or creative
        is_empty = not self.server.is_full((x, y))
        return can_reach and selected and is_empty

    def can_break(self, x, y):
        can_reach = self.can_reach(x, y)
        creative = self.mode in ["creative"]
        break_cooled_down = self.break_cooldown.expired() or creative
        return self.server.collides((x, y)) and can_reach and break_cooled_down

    def collect_item(self, item):
        self.inventory[item] = self.inventory.get(item, 0) + 1
    
    def break_(self, x, y):
        if self.server.get_tile((x, y)) is not None:
            tile = self.server.get_tile((x, y))
            tile_name = tile_names[type(tile)]
            self.server.set_tile((x, y), None)
            self.break_cooldown.start(tile.BREAK_COOLDOWN)
            survival = self.mode in ["survival"]
            if survival:
                self.collect_item(tile_name)

    def can_reach(self, x, y):
        distance = sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        creative = self.mode in ["creative"]
        return creative or distance < self.reach

    def selected_item(self):
        if self.inventory:
            return sorted(self.inventory)[0]
        return None

    def place(self, x, y, item):
        if self.server.get_tile((x, y)) is None:
            survival = self.mode in ["survival"]
            if survival:
                self.inventory[item] -= 1
                if self.inventory[item] == 0:
                    del self.inventory[item]
            self.server.set_tile((x, y), tile_names.inverse[item]())
    
    def get_type(self):
        return 1
    