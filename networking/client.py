import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999

client_socket.connect((host, port))

msg = client_socket.recv(2048)
client_socket.close()
print(msg.decode("ascii"))
