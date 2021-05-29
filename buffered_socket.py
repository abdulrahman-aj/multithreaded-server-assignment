import socket


class BufferedSocket:
    HEADER_SIZE = 10
    BUFFER_SIZE = 1024

    def __init__(self, family=socket.AF_INET, conn_type=socket.SOCK_STREAM, orig=None):
        if orig:
            assert isinstance(orig, socket.socket)
            self.sock = orig
        else:
            self.sock = socket.socket(family, conn_type)

    def accept(self):
        conn, addr = self.sock.accept()
        return BufferedSocket(orig=conn), addr

    def bind(self, address):
        return self.sock.bind(address)

    def close(self):
        self.sock.close()

    def connect(self, server):
        return self.sock.connect(server)

    def send(self, msg: bytes):
        header = f"{len(msg):0{BufferedSocket.HEADER_SIZE}}".encode("utf-8")

        msg = header + msg
        self.sock.send(msg)

    def recv(self) -> bytes:
        msg_length = b""
        while len(msg_length) < BufferedSocket.HEADER_SIZE:
            recv_length = BufferedSocket.HEADER_SIZE - len(msg_length)
            recv_length = min(recv_length, BufferedSocket.BUFFER_SIZE)
            msg_length += self.sock.recv(recv_length)

        msg_length = int(msg_length.decode("utf-8"))
        msg = b""
        while len(msg) < msg_length:
            recv_length = msg_length - len(msg)
            recv_length = min(recv_length, BufferedSocket.BUFFER_SIZE)
            msg += self.sock.recv(recv_length)

        assert len(msg) == msg_length
        return msg

    def listen(self, backlog=None):
        if not backlog:
            return self.sock.listen()

        assert isinstance(backlog, int)
        return self.listen(backlog)
