from tiles.tile import Tile


class Leaves(Tile):
    BREAK_COOLDOWN = 0.1
    
    def get_type(self):
        return 3
