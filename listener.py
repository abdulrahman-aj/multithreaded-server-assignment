import socket
import threading
import sys
from buffered_socket import BufferedSocket


class Listener:

    def __init__(self, host, port, client_handler):
        self.host = host
        self.port = port
        self.cliend_handler = client_handler
        self.sock = BufferedSocket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.running = False

    def listen(self):
        print("Server listening on {}:{}...".format(self.host, self.port))
        self.sock.listen()
        self.running = True
        while self.running:
            conn, addr = self.sock.accept()
            print(f"Connection from {addr[0]}:{addr[1]} established!",
                  file=sys.stderr)

            t = threading.Thread(target=self.cliend_handler, args=[conn, addr])
            t.start()

    def close(self):
        self.running = False
        self.sock.close()
