"""This module is responsible for creating and handling server socket"""

import socket
from _thread import start_new_thread

from router import router
from config import BIND_ADDRESS, BIND_PORT

class Server():
    """Socket server class for providing socket connection and its appropriate methods
    methods:
        new_connection
        accept_connections
    """
    def __init__(self, bind_address, port):
        """Constuctor method to initiate the instance"""
        self.bind_address = bind_address
        self.port = port

    def new_connection(self, conn):
        """Creates a new threaded socket connection to handle client
        This method recieves data from client
        Processes the data and sends to Router class
        Returns the response back to client
        """
        while True:
            data = conn.recv(2048)
            if not data:
                break

            response = router.request(data.decode())
            conn.sendall(response.encode())
        conn.close()

    def accept_connections(self):
        """This method creates and starts a socket server
        Waits for clients to connect
        Each client connection will be started in a new thread
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.bind_address, self.port))
            s.listen()
            print(f"Sever started on {self.bind_address}:{self.port}\n")

            while True:
                client, address = s.accept()
                print('Connected from ' + address[0] + ':' + str(address[1]))
                start_new_thread(self.new_connection, (client, ))

server = Server(BIND_ADDRESS, BIND_PORT)
server.accept_connections()
