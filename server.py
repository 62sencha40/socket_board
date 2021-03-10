import socket
from datetime import datetime
from concurrent import futures


HOST_IP = "0.0.0.0"
HOST_PORT = 8081
MAX_LISTEN = 5
BUFF = 1024

MSG_LIST = []
CON_LIST = []
CON_LOG = []


def send_massage_other_client(client_info: tuple, massage: str, no):
    b_ip = client_info[0].encode()
    b_port = str(client_info[1]).encode()
    b_massage = massage.encode()

    for i in range(len(CON_LIST)):
        if i != no:
            CON_LIST[i].send(b"from: [" + b_ip + b":" + b_port + b"] > " + b_massage)


def monitor_msg_list():
    now_msg_list_len = len(MSG_LIST)
    current_msg_list_len = now_msg_list_len

    while True:
        now_msg_list_len = len(MSG_LIST)
        if now_msg_list_len != current_msg_list_len:
            print(MSG_LIST[-1])

        current_msg_list_len = now_msg_list_len


def receive_massage(connection: socket.socket, client_info, no: int):
    send_massage_other_client(client_info, "in {}".format(client_info), no)

    while True:
        massage = connection.recv(BUFF).decode()
        if massage == "\r\n":
            CON_LIST.remove(CON_LOG[no])
            connection.close()

        MSG_LIST.append((massage, client_info[0], client_info[1]))
        send_massage_other_client(client_info, massage, no)


def socket_server():
    access_count = 0

    executor = futures.ThreadPoolExecutor(8)
    executor.submit(monitor_msg_list)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST_IP, HOST_PORT))
    server.listen(MAX_LISTEN)

    print("[{}] Server startup".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    try:
        while True:
            connection, client_info = server.accept()

            CON_LOG.append(connection)
            CON_LIST.append(connection)

            executor.submit(receive_massage, connection, client_info, access_count)

            access_count += 1

    except KeyboardInterrupt:
        print("[{}] Server stop".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


def main():
    socket_server()


if __name__ == '__main__':
    main()

