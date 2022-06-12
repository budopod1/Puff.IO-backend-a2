from math import floor, ceil
from shortsocket import Array


class Client:
    def __init__(self, user):
        self.user = user
        self.remembered_tilemap = {}
        self.max_ratio = 3
        self.veiw_height = 7
        self.veiw_width = self.max_ratio * self.veiw_height
        self.veiw_buffer = 1

    def change_server(self, new_server):
        self.user.change_server(new_server)
        self.remembered_tilemap = {}

    def render(self): # fix changing server
        player_x = self.user.player.x
        player_y = self.user.player.y
        seen_tiles = [
            (x, y)
            for x in range(
                floor(player_x - self.veiw_width) 
                - self.veiw_buffer,
                ceil(player_x + self.veiw_width) 
                + 1 + self.veiw_buffer
            )
            for y in range(
                floor(player_y - self.veiw_height) 
                - self.veiw_buffer,
                ceil(player_y + self.veiw_height) 
                + 1 + self.veiw_buffer
            )
        ]
        
        send_tiles = []
        for tile_pos in seen_tiles:
            if (tile_pos not in self.remembered_tilemap or
                    self.remembered_tilemap[tile_pos]
                    != self.user.server.get_tile(tile_pos)):
                real_tile = self.user.server.get_tile(tile_pos)
                self.remembered_tilemap[tile_pos] = real_tile
                send_tiles.append((
                    tile_pos,
                    real_tile.get_type() if real_tile else 0
                ))
        
        entities = self.user.server.entities
        return Array([
            Array([tile[0][0] for tile in send_tiles], dtype="int32"),
            Array([tile[0][1] for tile in send_tiles], dtype="int32"),
            Array([tile[1] for tile in send_tiles], dtype="int8"),
            Array([entity.x for entity in entities], dtype="float32"),
            Array([entity.y for entity in entities], dtype="float32"),
            Array([entity.get_type() for entity in entities], dtype="int8"),
            Array([player_x, player_y], dtype="float32")
        ])
