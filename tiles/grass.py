from tiles.tile import Tile


class Grass(Tile):
    BREAK_COOLDOWN = 0.2
    
    def get_type(self):
        return 1
