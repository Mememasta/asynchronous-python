import socket
from select import select


tasks = []

to_read = {}
to_write = {}

def server():
    server_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_soket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_soket.bind(('localhost', 8083))
    server_soket.listen()

    while True:

        yield ('read', server_soket)
        client_socket, addr = server_soket.accept()

        print("Connection from", addr)

        tasks.append(client(client_socket))


def client(client_socket):
    while True:

        yield ('read', client_socket)
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = "Hello World\n".encode()

            yield ('write', client_socket)
            client_socket.send(response)

    client_socket.close()

def event_loop():

    while any([tasks, to_read, to_write]):

        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)

            reason, sock = next(task)
            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
        except StopIteration:
            print('done')


tasks.append(server())
event_loop()