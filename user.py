from entities.player import Player


class User:
    def __init__(self, server, username):
        self.player = Player(server, (0, 2))
        self.server = None
        self.change_server(server)
        self.username = username

    def change_server(self, server):
        if self.server:
            self.server.entities.remove(self.player)
        # Make player store position over locations
        server.entities.append(self.player)
        self.server = server
