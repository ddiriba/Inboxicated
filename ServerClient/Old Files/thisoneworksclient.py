#importing deez nuts
import socket
import os
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = socket.gethostbyname("renoxdeception.duckdns.org")

port = 10050 # Port to listen on (non-privileged ports are > 1023)
client_socket.connect((host_ip,port)) 

data =  open(os.getcwd() + '/nice_dog.jpg', 'rb') 
packet_sent = data.read(4096)
    
while packet_sent:
    client_socket.send(packet_sent)
    packet_sent = data.read(4096)
    
    
client_socket.close()
data.close()