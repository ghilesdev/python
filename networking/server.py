import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999
server_socket.bind((host, port))

server_socket.listen(10)

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {str(addr)}")
    msg = "thanks for connecting\r\n"
    client_socket.send(msg.encode("ascii"))
    client_socket.close()
