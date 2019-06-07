import socket

#domain: 8000


server_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_soket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_soket.bind(('localhost', 8000))
server_soket.listen()

while True:
    client_socket, addr = server_soket.accept()
    print("Connection from", addr)
    
    while True:
        request = client_socket.recv(4096)
        
        if not request:
            break
        else:
            response = "Hello World\n".encode()
            client_socket.send(response)
            
    client_socket.close()
    