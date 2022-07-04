from tiles.tile import Tile


class Wood(Tile):
    COLLISION = False
    BREAK_COOLDOWN = 0.5
    
    def get_type(self):
        return 2
