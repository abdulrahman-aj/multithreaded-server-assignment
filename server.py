#!/usr/bin/env python
import json
import sys
import signal
from listener import Listener
from matrix import Matrix


matrix = Matrix()


def main():
    with open("config.json", "r") as f:
        confjson = json.load(f)

    host = confjson["HOST"]
    port = confjson["PORT"]

    server = Listener(host, port, client_handler)

    def signal_handler(sig, frame):
        print("\nterminated...")
        server.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    server.listen()


def client_handler(conn, addr):
    print(f"Established connection from {addr}!")

    methods = {
        "sum": Matrix.sum,
        "sort": Matrix.sort,
        "max": Matrix.max,
        "transpose": Matrix.transpose,
        "count": Matrix.count
    }

    while True:
        try:
            request = conn.recv().decode("utf-8")
        except BrokenPipeError:
            break

        if not request:
            break

        response = {}

        if request not in methods:
            response["status"] = "invalid"
        else:
            response["status"] = "success"
            response[request] = methods[request](matrix)

        msg = json.dumps(response).encode("utf-8")

        try:
            conn.send(msg)
        except BrokenPipeError:
            break

    conn.close()


if __name__ == "__main__":
    main()
