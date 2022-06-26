from tiles.tile import Tile


class Flowers(Tile):
    COLLISION = False
    
    def get_type(self):
        return 5
