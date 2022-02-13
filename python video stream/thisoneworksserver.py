#importing libraries
import socket
import struct

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = "10.0.0.3"
print('HOST IP:',host_ip)
port = 10050
socket_address = (host_ip,port)
print('Socket created')

server_socket.bind(socket_address)
print('Socket bind complete')
server_socket.listen(5)
print('Socket now listening')

payload_size = struct.calcsize("Q")
data = b""

client_socket,addr = server_socket.accept()
file_recieved = open("dawitsfile.jpg", "wb")
recieved_packet = client_socket.recv(4096)

while recieved_packet:
    file_recieved.write(recieved_packet)
    recieved_packet = client_socket.recv(4096)