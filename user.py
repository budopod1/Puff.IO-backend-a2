from entities.player import Player
from math import floor, ceil
from shortsocket import Array
from timer import Stopwatch
from functools import lru_cache


class User:
    def __init__(self, server, username):
        self.player = Player(server, (0, 2), user=self)
        self.server = None
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
        incremented = 0
        while new_id in self.used_ids:
            new_id += 1
            incremented = 1
            if incremented == 15:
                break
        return new_id

    def check_entity_ids(self):
        for i in range(16):
            ids_for_etype = [
                i * 16 - 126 + j in self.used_ids 
                for j in range(16)
            ]
            if all(ids_for_etype):
                self.used_ids = []
                self.get_id.clear_cache()
                return

    def change_server(self, server):
        if self.server:
            self.server.entities.remove(self.player)
        # Make player store position over locations
        server.entities.append(self.player)
        self.server = server
        self.remembered_tilemap = {}
    
    def render_frame(self): # fix changing server
        self.timer.start()

        self.check_entity_ids()
        entities = {
            id(entity): (entity.x, entity.y,
                         self.get_entity_id(entity))
            for entity in self.server.entities
            if entity.enabled
        }
        
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
        
        player_index = None
        for i, (entity_id, _) in enumerate(entities.items()):
            if entity_id == id(self.player):
                player_index = i
                
        entities = [
            (x, y, etype)
            for _, (x, y, etype) in entities.items()
            if x_min <= x <= x_max
            if y_min <= y <= y_max
        ]

        return Array([
            Array([tile[0][0] for tile in send_tiles], dtype="int32"),
            Array([tile[0][1] for tile in send_tiles], dtype="int32"),
            Array([tile[1] for tile in send_tiles], dtype="int8"),
            Array([entity[0] for entity in entities], dtype="float32"),
            Array([entity[1] for entity in entities], dtype="float32"),
            Array([entity[2] for entity in entities], dtype="int8"),
            Array([player_index], dtype="int8")
        ])
    
    def client_frame(self, keys):
        # self.timer.tick()
        self.keys_just_down = keys - self.keys_just_down
        self.keys_down = keys

    def state_frame(self):
        # print(self.timer.time())
        self.player.enabled = self.timer.time() < 10
