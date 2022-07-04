from tiles.tile import Tile


class Stone(Tile):
    BREAK_COOLDOWN = 2
    
    def get_type(self):
        return 4
