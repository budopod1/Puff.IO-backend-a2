from server import Server
# from client import Client
from user import User
from timer import Timer
# from time import sleep


class State:
    def __init__(self):
        self.users = {}
        self.servers = []
        self.main_server = self.add_server()

        self.timer = Timer()

    def add_server(self):
        new_server = Server(self)
        self.servers.append(new_server)
        return new_server

    def create_user(self, username):
        assert username not in self.users, f"User {username} already exists"
        new_user = User(self.main_server, username)
        self.users[username] = new_user
        return new_user

    def tick(self):
        self.timer.tick()
        
        for server in self.servers:
            server.tick()
            
        for user in list(self.users.values()):
            user.state_frame()
