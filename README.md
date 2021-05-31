# Multithreaded Server ASsignment
### Name: Abdulrahman Ajlouni.
### ID: 133571.

## Files:
```
.
├── buffered_socket.py
├── client.py
├── config.json
├── listener.py
├── matrix.py
├── server.py
└── README.md
```

### buffered_socket.py
 - Wrapper class around the standard python socket, same functionality as standard socket with buffering handled.

### client.py
 - client CLI.

### config.json
 - Contains ip and port on which the server will run on.

### listener.py
 - Server listener, handles creating threads to serve clients, takes a client_handler function in the constructor.

### matrix.py
 - Thread-safe (Monitor) matrix class.

### server.py
 - Server code, contains client_handler.


## Notes:
 - Because of GIL, only one thread is allowed to take control of the python interpreter; and thus the server only utilizes concurrency and does not utilize parallelism.

 - Response time = 0.0015  on average.
