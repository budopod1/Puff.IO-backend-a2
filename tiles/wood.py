from tiles.tile import Tile


class Wood(Tile):
    COLLISION = False
    
    def get_type(self):
        return 2
