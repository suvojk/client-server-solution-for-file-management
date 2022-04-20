"""This module is responsible for creating and handling client socket"""

import socket
import json
from config import CONNECTION_ADDRESS, CONNECTION_PORT

class Client():
    """Class to provide Client Socket connection and required methods
    methods:
        connect
        send
        close
    """
    def __init__(self, connection_address, port):
        """constructor method to initiate instance"""
        self.connection_address = connection_address
        self.port = port
        self.token = ""
        self.socket_obj = ""

    def connect(self):
        """Creates a socket connection
        Takes Address and port of server to connect"""
        socket_obj = socket.socket()
        socket_obj.connect((self.connection_address, self.port))
        self.socket_obj = socket_obj

    def send(self, body):
        """Sends request along with the given data to server
        Returns the response came from the server
        """

        # add token if exists
        body['token'] = self.token

        body = json.dumps(body)
        self.socket_obj.sendall(body.encode())
        response = self.socket_obj.recv(1024)

        # add token to user
        response_dict = json.loads(response.decode())
        if 'token' in response_dict:
            self.token = response_dict['token']

        return response_dict
        # self.socket_obj.close()

    def close(self):
        """Closes the socker connection"""
        self.socket_obj.close()

client = Client(CONNECTION_ADDRESS, CONNECTION_PORT)
client.connect()
