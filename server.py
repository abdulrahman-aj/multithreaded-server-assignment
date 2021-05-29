import socket
import threading
import json
import sys
from buffered_socket import BufferedSocket


class Server:

    def __init__(self, host, port, handler):
        self.host = host
        self.port = port
        self.handler = handler
        self.sock = BufferedSocket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))

    def run(self):
        print("Server running on {}:{}...".format(self.host, self.port))
        self.sock.listen()
        while True:
            conn, addr = self.sock.accept()
            print(f"Connection from {addr[0]}:{addr[1]} established!",
                  file=sys.stderr)

            t = threading.Thread(target=self.handler, args=[conn, addr])
            t.start()

    def close(self):
        raise NotImplementedError()
