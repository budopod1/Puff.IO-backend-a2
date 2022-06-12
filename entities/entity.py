class Entity:
    def __init__(self, server, pos=(0, 0)):
        self.x, self.y = pos
        self.server = server
        self.state = server.state

    def get_type(self):
        return 0

    def tick(self):
        pass
