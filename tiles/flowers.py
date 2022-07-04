from tiles.tile import Tile


class Flowers(Tile):
    COLLISION = False
    BREAK_COOLDOWN = 0
    
    def get_type(self):
        return 5
