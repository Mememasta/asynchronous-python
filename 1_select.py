import socket
from select import select
# domain: 8000


#файловый дискриптор .fileno()

to_monitor = []

server_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_soket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_soket.bind(('localhost', 8000))
server_soket.listen()

def accept_connection(sercer_socket):
        client_socket, addr = server_soket.accept()
        print("Connection from", addr)

        to_monitor.append(client_socket)

def send_message(client_socket):
        request = client_socket.recv(4096)

        if request:
            response = "Hello World\n".encode()
            client_socket.send(response)
        else:
            client_socket.close()

def event_loop():
    while True:

        ready_to_read, _, _ = select(to_monitor, [], [])

        for sock in ready_to_read:
            if sock is server_soket:
                accept_connection(sock)
            else:
                send_message(sock)

if __name__ == '__main__':
    to_monitor.append(server_soket)
    #accept_connection(server_soket)
    event_loop()
