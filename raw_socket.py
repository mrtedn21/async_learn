import selectors
import socket

selector = selectors.DefaultSelector()

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('localhost', 8001)
server_socket.setblocking(False)
server_socket.bind(server_address)
server_socket.listen()

selector.register(server_socket, selectors.EVENT_READ)

while True:
    events = selector.select(timeout=100)

    if len(events) == 0:
        print('There are now events yet')

    for event, _ in events:
        event_socket = event.fileobj

        if event_socket == server_socket:
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print('Gettiing request for connection, address')
            print(address)
            selector.register(connection, selectors.EVENT_READ)
        else:
            data = event_socket.recv(1024)
            print('Getting data:')
            print(data)
            event_socket.send(data)
