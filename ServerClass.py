#imself.porting deez nuts
import socket
import os


#should be used by the pi
class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host_ip = socket.gethostbyname("renoxdeception.duckdns.org")
        self.port = 10050 # self.port to listen on (non-privileged self.ports are > 1023)

        
    def send_image(self, file_location):
        self.client_socket.connect((self.host_ip,self.port)) 
        #insert file location
        file_location = os.getcwd() + '/nice_dog.jpg'
        data =  open(file_location, 'rb') 
        
        packet_sent = data.read(4096)
        
        while packet_sent:
            self.client_socket.send(packet_sent)
            packet_sent = data.read(4096)
            
        self.client_socket.close()
        
    def send_value(self, value):
        #value would be string/int/bool
        self.client_socket.connect((self.host_ip,self.port)) 
        self.client_socket.send(value.encode())
        self.client_socket.close()
        
    def receive_value(self):
        #should get bool/string values telling us algorithm is correct
        #or not
        self.client_socket.connect((self.host_ip,self.port)) 
        received_packet = self.client_socket.recv(1024)
        print(received_packet.decode())
        return received_packet.decode()
        
#should be used by the computer
class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host_ip = "10.0.0.3" #not sure if this is constant, keep an eye
        self.port = 10050
        self.socket_address = (self.host_ip,self.port)
        
        
    def revieve_image(self):
        self.server_socket.bind(self.socket_address)
        self.server_socket.listen(5)
        self.client_socket,addr = self.server_socket.accept()
        #we need to figure out how to put correct names of files
        file_recieved = open("dawitsfile.jpg", "wb")
        recieved_packet = self.client_socket.recv(4096)
        
        while recieved_packet:
            file_recieved.write(recieved_packet)
            recieved_packet = self.client_socket.recv(4096)
        
    def recieve_value(self):
        self.server_socket.connect((self.host_ip,self.port)) 
        received_packet = self.server_socket.recv(1024)
        print(received_packet.decode())
        return received_packet.decode()

