import functools
import selectors
import socket
from selectors import BaseSelector


class CustomFuture:
    def __init__(self):
        self._result = None
        self._is_finished = None
        self._done_callback = None

    def result(self):
        return self._result

    def is_finished(self):
        return self._is_finished

    def set_result(self, result):
        self._result = result
        self._is_finished = True
        if self._done_callback:
            self._done_callback(result)

    def add_done_callback(self, fn):
        self._done_callback = fn

    def __await__(self):
        if not self._is_finished:
            yield self
        return self.result()


def accept_connection(future: CustomFuture, connection: socket):
    print(f'get request for connection from {connection}')
    future.set_result(connection)


async def sock_accept(sel: BaseSelector, sock) -> socket:
    print('Registration socket for listening')
    future = CustomFuture()
    sel.register(
        sock,
        selectors.EVENT_READ,
        functools.partial(accept_connection, future)
    )
    print('Listen requests for connection')
    connection: socket = await future
    return connection


async def main(sel: BaseSelector):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('localhost', 8001))
    sock.listen()
    sock.setblocking(False)

    print('Wait connections for socket')
    connection = await sock_accept(sel, sock)
    print(f'Get connection {connection}')


if __name__ == '__main__':
    selector = selectors.DefaultSelector()

    coro = main(selector)

    while True:
        try:
            state = coro.send(None)

            events = selector.select()

            for key, mask in events:
                print('Handle events of selector')
                callback = key.data
                callback(key.fileobj)
        except StopIteration as si:
            print('App finish')
            break

