from entities.entity import Entity
from math import sqrt, ceil
from tiles import tile_names, tile_order
from timer import Cooldown
from gui import trade_guis, get_trade


class Player(Entity):
    def __init__(self, *args, user=None):
        super().__init__(*args)
        assert user
        self.user = user

        self.health = 10
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

        self.mouse_x = 0
        self.mouse_y = 0
        self.keys = set()
        self.keys_just_down = set()

        self.reach = 4

        self.inventory = {}
        self.selected = 1

        # I stole the names from minceraft, so what?
        self.mode = "survival"

        self.ground_pounding = False
        self.ground_pound_speed = -10

        self.break_cooldown = Cooldown()

    def damage(self, amount):
        if self.mode in ["survival"]:
            super().damage(amount)

    def get_health(self):
        if self.mode in ["creative"]:
            return 0
        else:
            return ceil(self.health * 2)

    def tick(self):
        if not super().tick():
            return False

        self.user.proccess_input()
        
        press_ground_pound = 83 in self.user.keys_just_down
        press_jump = 87 in self.user.keys_down
        up_and_down = press_ground_pound and press_jump

        if 69 in self.user.keys_just_down:
            if self.user.gui == 0:
                self.user.gui = 1
            else:
                self.user.gui = 0
        elif 27 in self.user.keys_just_down:
            self.user.gui = 0
            
        mouse_buttons = self.user.mouse_buttons
        mouse_buttons_just_down = self.user.mouse_buttons_just_down

        if (self.user.gui in trade_guis and self.user.cell >= 0
            and 1 in mouse_buttons_just_down):
            cell = self.user.cell
            i = 0
            while cell > 3:
                cell -= 4
                if i % 2 == 0:
                    cell -= 1
                i += 1
            trade = get_trade(self.user.gui, i)
            if trade is not None:
                if self.try_trade(trade):
                    self.user.gui = 0
                    # mouse is still in same place as when clicked on trader
                    # as far as game knows, so if we don't remove the mouse input
                    # the gui will immediatly reopen
                    mouse_buttons = set()
                    mouse_buttons_just_down = set()
        
        if self.user.gui:
            return

        time_delta = self.state.timer.time_delta

        self.damage(time_delta / 2)

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
        
        if 1 in mouse_buttons:
            if self.can_place(mouse_x, mouse_y):
                self.place(mouse_x, mouse_y, self.selected_item())
            elif 1 in mouse_buttons_just_down and\
                    self.can_interact(mouse_x, mouse_y):
                self.interact(mouse_x, mouse_y)

        if 3 in mouse_buttons and self.can_break(mouse_x, mouse_y):
            self.break_(mouse_x, mouse_y)

        self.selected += self.user.scroll
        self.user.scroll = 0
        if self.selected >= max(tile_order):
            self.selected = 1
        elif self.selected <= 0:
            self.selected = len(tile_order) - 1

    def get_break_speed(self):
        return max([
            tile_names.inverse[item].BREAK_SPEED
            for item in self.inventory
        ], default=1)

    def try_trade(self, trade):
        take, give = trade
        for item, amount in take:
            name = tile_names[item]
            if not self.has_n_items(name, amount):
                return False
        for item, amount in take:
            name = tile_names[item]
            self.remove_n_items(name, amount)
        item, amount = give
        name = tile_names[item]
        self.add_n_items(name, amount)
        return True

    def can_interact(self, x, y):
        tile = self.server.get_tile((x, y))
        if tile:
            return tile.INTERACTABLE

    def interact(self, x, y):
        tile = self.server.get_tile((x, y))
        if tile:
            tile.interact(self)

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

    def sorted_inventory(self):
        return sorted(
            self.inventory,
            key=lambda k: tile_order.inverse[tile_names.inverse[k]]
        )

    def remove_n_items(self, item, n):
        assert self.has_n_items(item, n)
        curr_num = self.inventory[item]
        if curr_num - n > 0:
            self.inventory[item] = curr_num - n
        else:
            del self.inventory[item]

    def has_n_items(self, item, n):
        return self.inventory.get(item, 0) >= n

    def add_n_items(self, item, n):
        if item not in self.inventory:
            self.inventory[item] = n
        else:
            self.inventory[item] += n

    def collect_item(self, item):
        self.add_n_items(item, 1)
    
    def break_(self, x, y):
        if self.server.get_tile((x, y)) is not None:
            tile = self.server.get_tile((x, y))
            self.server.set_tile((x, y), None)
            self.break_cooldown.start(
                tile.BREAK_COOLDOWN / self.get_break_speed()
            )
            survival = self.mode in ["survival"]
            if survival:
                self.collect_item(tile_names[tile.turn_to()])

    def can_reach(self, x, y):
        distance = sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        creative = self.mode in ["creative"]
        return creative or distance < self.reach

    def selected_item(self):
        if self.inventory:
            item = tile_names[tile_order[self.selected]]
            return item if item in self.inventory else None
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
    