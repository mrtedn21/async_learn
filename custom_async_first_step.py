import functools
import selectors
import socket
from selectors import BaseSelector


registered_coroutines = []


class CustomFuture:
    def __init__(self):
        print('init of future')
        self._result = None
        self._is_finished = None
        self._done_callback = None
        print('init of future finished')

    def result(self):
        print('returning result')
        print(f'result: {str(self._result)}')
        return self._result

    def is_finished(self):
        print('is_finished function')
        print(f'is_finished: {self._is_finished}')
        return self._is_finished

    def set_result(self, result):
        print('setting the result')
        print(f'result: {str(result)}')
        self._result = result
        self._is_finished = True
        if self._done_callback:
            print('there is callback')
            print(f'callback: {str(callback)}')
            self._done_callback(result)
            print('callback is finished')
        else:
            print('there is no callback')

    def add_done_callback(self, fn):
        print('add_done_callback')
        print(f'function is {str(fn)}')
        self._done_callback = fn

    def __await__(self):
        while True:
            print('await working')
            print(f'self future is {self}')
            print(f'self._is_finished is {self._is_finished}')
            if not self._is_finished:
                print('await is yielded')
                yield self
            else:
                print('await working after yield and ready to return result')
                return self.result()


def accept_connection(future: CustomFuture, connection: socket):
    print('accept_connection function is begin to run')
    print(f'connection: {connection}')
    print(f'future: {future}')
    client_socket, client_address = connection.accept()
    client_socket.setblocking(False)
    future.set_result((client_socket, client_address))


def receive_data(future: CustomFuture, client_socket: socket):
    print(f'receive_data function works with socket: {client_socket}')
    result = b''
    while True:
        try:
            data = client_socket.recv(3)
        except BlockingIOError:
            break
        result += data
    print('HAVE GOT DATA')
    print('_____________')
    print(result)
    print('_____________')
    print('HAVE GOT DATA')
    future.set_result(result)


def register_connection_in_selector(sel: BaseSelector, sock, callback) -> socket:
    print(f'register_connection_in_selector function. sel: {str(sel)}, sock: {str(sock)}')
    future = CustomFuture()
    try:
        sel.get_key(sock)
    except KeyError:
        sel.register(
            sock,
            selectors.EVENT_READ,
            functools.partial(callback, future),
        )
    else:
        sel.modify(
            sock,
            selectors.EVENT_READ,
            functools.partial(callback, future),
        )
    print('socket was registered in selector')
    return future


async def listen_client(sel, client_socket):
    print('listen_client coroutine')
    while True:
        print('infinite loop of listen_client_coroutine')
        client_connection_future = register_connection_in_selector(sel, client_socket, receive_data)
        print('got result of register function')
        print(f'this result is client_connection_future: {client_connection_future}')
        await client_connection_future
        print('await of listen_client worked')


async def main(sel: BaseSelector):
    print('main function run')
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('localhost', 8001))
    sock.listen()
    sock.setblocking(False)
    print('socket is created')

    while True:
        print('in infinite loop of main coroutine')
        connection_future = register_connection_in_selector(sel, sock, accept_connection)
        print(f'get connection {connection_future}')
        client_socket, client_address = await connection_future
        print(f'result of future - {client_socket, client_address}')

        global registered_coroutines
        print('got global registered_coroutines')
        print(f'registered_coroutines: {registered_coroutines}')
        registered_coroutines.append(listen_client(sel, client_socket))


if __name__ == '__main__':
    print('the program start')
    selector = selectors.DefaultSelector()
    print('selector got')

    coro = main(selector)
    print('coroutine was made')

    while True:
        print('in infinite loop of the program')
        try:
            state = coro.send(None)
            print('coroutine was send')
            for coroutine in registered_coroutines:
                print('for coro in registered_coroutines')
                print(f'registered_coroutines: {registered_coroutines}')
                coroutine.send(None)
                print(f'coro: {coroutine} was send')

            events = selector.select()
            print('selector give the events')

            for key, mask in events:
                print('handle events of selector')
                callback = key.data
                print(f'callback is {str(callback)}')
                print(f'file obj is {str(key.fileobj)}')
                callback(key.fileobj)
                print('callback was executed')
        except StopIteration as si:
            print('App finish')
            break
