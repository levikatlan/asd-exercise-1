import socket
import struct
import time


def upload_thought(address: tuple, user_id: int, thought: str) -> None:
    """
    Connects to address and uploads the thought of user_id using BinaryProtocol.
    BinaryProtocol is defined as:
    user_id (unit64/8 bytes): timestamp (unit64/8 bytes): thought_size (unit32/4 byted): thought_data: (unitN/N bytes)
    :param address: tuple where the first element is a string representing IPv4 and the second an int representing the port
    :param user_id: unique identifier for the user on the server
    :param thought: user thought data
    :return: None
    """

    client = socket.socket()
    try:
        thought_size = len(thought)
        message = struct.pack(f'<QQI{thought_size}s', user_id, int(time.time()), thought_size, thought.encode())

        with socket.socket() as client:
            client.connect(address)
            client.sendall(message)
    except Exception as e:
        print(f'Error in "upload_thought": {e}')
        raise e


def main(argv):
    if len(argv) != 4:
        print(f'USAGE: {argv[0]} <address> <user_id> <thought>')
        return 1
    try:
        _, address, user_id, thought = argv
        ip, port = address.split(':')
        upload_thought((ip, int(port)), int(user_id), thought)
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
