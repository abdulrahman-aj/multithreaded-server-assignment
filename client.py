#!/usr/bin/env python
import socket
import json
from buffered_socket import BufferedSocket


def main():
    with open("config.json", "r") as f:
        confjson = json.load(f)

    sock = BufferedSocket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((confjson["HOST"], confjson["PORT"]))

    methods = {
        "1": "sum",
        "2": "sort",
        "3": "max",
        "4": "transpose",
        "5": "count",
        "q": "quit"
    }

    prompt = "Select an operation:\n"
    for key, value in methods.items():
        prompt += key + ": " + value + "\n"

    while (method_id := input(prompt)) != "q":
        if method_id not in methods:
            continue

        method = methods[method_id]

        sock.send(method.encode("utf-8"))

        response = sock.recv().decode("utf-8")
        response = json.loads(response)

        print(f"\n{response}\n")

    print("\ndisconnecting...")
    sock.close()


if __name__ == "__main__":
    main()
