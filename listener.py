import socket
import threading
import sys
from buffered_socket import BufferedSocket


class Listener:

    def __init__(self, host, port, client_handler):
        """init server socket, bind on (host, port)"""
        self.host = host
        self.port = port
        self.cliend_handler = client_handler
        self.sock = BufferedSocket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.running = False

    def listen(self):
        """start listening for clients"""
        self.sock.listen()
        self.running = True
        while self.running:
            conn, addr = self.sock.accept()
            t = threading.Thread(target=self.cliend_handler, args=[conn, addr, lambda: self.running])
            t.start()

    def close(self):
        """free resources"""
        self.running = False
        self.sock.close()
