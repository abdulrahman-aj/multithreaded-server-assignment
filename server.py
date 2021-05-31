#!/usr/bin/env python
import json
import os
import signal
import socket
import sys
from listener import Listener
from matrix import Matrix
from threading import Lock


def main():
    """Server driver code"""

    # Load ip and port
    with open("config.json", "r") as f:
        confjson = json.load(f)

    # Initialize matrix to operate on
    matrix = Matrix()
    
    # Synchronized output with clear
    lock = Lock()
    def output():
        with lock:
            os.system("cls" if os.name == "nt" else "clear")
            print(matrix)

    # Client handler, wrapper to avoid global variables
    def handler(conn, addr, is_running): return client_handler(
        conn, addr, is_running, matrix, output
    )

    output()
    
    # Initialize listener
    listener = Listener(confjson["HOST"], confjson["PORT"], handler)

    # Close server with ^C, frees resources
    def signal_handler(sig, frame):
        listener.close()
        sys.exit(0)

    # Install ^C handler
    signal.signal(signal.SIGINT, signal_handler)

    # Start listening
    listener.listen()


def client_handler(conn, addr, is_running, matrix, output):
    """
    Recieves method calls from client and returns them as JSON
    """
    
    methods = {
        "sum": Matrix.sum,
        "sort": Matrix.sort,
        "max": Matrix.max,
        "transpose": Matrix.transpose,
        "count": Matrix.count
    }

    conn.settimeout(1)
    
    while is_running():
        try:
            while is_running():
                try:
                    request = conn.recv().decode("utf-8")
                    break
                except socket.timeout:
                    continue
        except BrokenPipeError:
            break

        if not request or request == "disconnect":
            break

        if request not in methods:
            response = {"status": "invalid"}
        else:
            response = {"status": "ok", request: methods[request](matrix)}
            output()

        msg = json.dumps(response).encode("utf-8")

        try:
            while True:
                try:
                    conn.send(msg)
                    break
                except:
                    continue
        except BrokenPipeError:
            break
    

    conn.close()


if __name__ == "__main__":
    main()
