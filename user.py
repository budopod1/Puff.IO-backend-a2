from entities.player import Player
from math import floor, ceil
from shortsocket import Array
from timer import Stopwatch
from functools import lru_cache


class User:
    def __init__(self, server, username):
        self.player = Player(server, (0, 0), user=self)
        self.server = None
        self.user_positions = {}
        self.change_server(server)
        self.username = username

        self.keys_down = set()
        self.keys_just_down = set()
        self.remembered_tilemap = {}
        self.max_ratio = 3
        self.veiw_height = 7
        self.veiw_width = self.max_ratio * self.veiw_height
        self.veiw_buffer = 1
        self.timer = Stopwatch()
        self.used_ids = []

    @lru_cache(maxsize=255)
    def get_entity_id(self, entity):
        new_id = entity.get_type() * 16 - 126
        return new_id

    def change_server(self, server):
        if self.server:
            self.user_positions[self.server] = (
                self.player.x, 
                self.player.y
            )
            self.server.entities.remove(self.player)
        if server in self.user_positions:
            self.player.x, self.player.y = self.user_positions[server]
        else:
            self.player.x = 0
            self.player.y = server.get_highest(0)
        # Make player store position over locations
        server.entities.append(self.player)
        self.server = server
        self.remembered_tilemap = {}
    
    def render_frame(self):
        self.timer.start()

        # self.check_entity_ids()
        entities = {
            id(entity): (entity.x, entity.y,
                         self.get_entity_id(entity))
            for entity in self.server.entities
            if entity.enabled
        }

        if id(self.player) not in entities:
            return None
        player_x, player_y, _ = entities[id(self.player)]
        
        x_min = (floor(player_x - self.veiw_width) 
                - self.veiw_buffer)
        x_max = (ceil(player_x + self.veiw_width) 
                + 1 + self.veiw_buffer)
        y_min = (floor(player_y - self.veiw_height) 
                - self.veiw_buffer)
        y_max = (ceil(player_y + self.veiw_height) 
                + 1 + self.veiw_buffer)
        
        seen_tiles = [
            (x, y)
            for x in range(x_min, x_max)
            for y in range(y_min, y_max)
        ]
        
        send_tiles = []
        for tile_pos in seen_tiles:
            if (tile_pos not in self.remembered_tilemap or
                    self.remembered_tilemap[tile_pos]
                    != self.server.get_tile(tile_pos)):
                real_tile = self.server.get_tile(tile_pos)
                self.remembered_tilemap[tile_pos] = real_tile
                send_tiles.append((
                    tile_pos,
                    real_tile.get_type() if real_tile else 0
                ))
                
        entities = {
            eid: (x, y, etype)
            for eid, (x, y, etype) in entities.items()
            if x_min <= x <= x_max
            if y_min <= y <= y_max
        }
        
        player_index = None
        for i, (entity_id, _) in enumerate(entities.items()):
            if entity_id == id(self.player):
                player_index = i

        return Array([
            Array([tile[0][0] for tile in send_tiles], dtype="int32"),
            Array([tile[0][1] for tile in send_tiles], dtype="int32"),
            Array([tile[1] for tile in send_tiles], dtype="int8"),
            Array([entity[0] for entity in entities.values()], dtype="float32"),
            Array([entity[1] for entity in entities.values()], dtype="float32"),
            Array([entity[2] for entity in entities.values()], dtype="int8"),
            Array([player_index], dtype="int8")
        ])
    
    def client_frame(self, keys):
        # self.timer.tick()
        self.keys_just_down = keys - self.keys_just_down
        self.keys_down = keys

    def state_frame(self):
        # print(self.timer.time())
        self.player.enabled = self.timer.time() < 10
