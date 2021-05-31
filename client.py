#!/usr/bin/env python
import socket
import signal
import json
from buffered_socket import BufferedSocket

def signal_handler(sig, frame):
    return


def main():
    
    # This prevents the client from exiting with ^C, to free resources properly.
    signal.signal(signal.SIGINT, signal_handler)

    # Load ip and port
    with open("config.json", "r") as f:
        confjson = json.load(f)

    # Client socket
    sock = BufferedSocket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((confjson["HOST"], confjson["PORT"]))

    # Remote procedures
    methods = {
        "1": "sum",
        "2": "sort",
        "3": "max",
        "4": "transpose",
        "5": "count",
        "d": "disconnect"
    }

    # User prompt
    prompt = "Select an operation:\n"
    for key, value in methods.items():
        prompt += key + ": " + value + "\n"
    
    # Communication loop
    while True:
        method_id = input(prompt).lower()
        if method_id not in methods:
            continue

        method = methods[method_id]
        sock.send(method.encode("utf-8"))

        if method_id == "d":
            break

        response = sock.recv().decode("utf-8")
        response = json.loads(response)

        print(f"\n{response}\n")

    print("\ndisconnecting...")
    sock.close()


if __name__ == "__main__":
    main()
