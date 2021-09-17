import socket
import struct
import time
from datetime import datetime as dt

_READ_BUFFER = 4096


def run_server(address: tuple) -> None:
    _HEADER_FORMAT = '<QQI'
    _HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)
    _HANDLING_DELAY_SECONDS = 1

    try:
        with socket.socket() as server:
            server.bind(address)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.listen()

            while True:
                client, client_address = server.accept()
                data = read_data(client)
                user_id, timestamp, thought_size = struct.unpack(_HEADER_FORMAT, data[:_HEADER_SIZE])
                thought = struct.unpack(f'{thought_size}s', data[_HEADER_SIZE:])[0]
                time.sleep(_HANDLING_DELAY_SECONDS)
                print(f'[{dt.fromtimestamp(timestamp).strftime("%F %H:%M:%S")}] user {user_id}: {thought.decode()}')
    except Exception as e:
        print(f'Error in "run_server": {e}')
        raise e


def read_data(connection: socket.socket, buffer_size: int = _READ_BUFFER) -> bytes:
    data = b''
    while new_data := connection.recv(buffer_size):
        if not new_data:
            break
        data += new_data
    return data


def main(argv):
    if len(argv) != 2:
        print(f'USAGE: {argv[0]} <address>:<port>')
        return 1
    try:
        _, address = argv
        ip, port = address.split(':')
        run_server((ip, int(port)))
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
