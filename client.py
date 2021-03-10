import socket


DEST_IP = "127.0.0.1"
DEST_PORT = 8081


def socket_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((DEST_IP, DEST_PORT))
    client.send(b"aiueo")


def main():
    socket_client()


if __name__ == '__main__':
    main()
