#importing libraries
import socket
import cv2
import pickle
import struct
import imutils

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = socket.gethostbyname("renoxdeception.duckdns.org")

port = 10050 # Port to listen on (non-privileged ports are > 1023)
# now connect to the web server on the specified port number
client_socket.connect((host_ip,port)) 
#'b' or 'B'produces an instance of the bytes type instead of the str type
#used in handling binary data from network connections
data = b""
# Q: unsigned long long integer(8 bytes)
payload_size = struct.calcsize("Q")

while True:
    packet = client_socket.send(4*1024)
    if not packet: break
    else:
        data += packet
        vid = cv2.VideoCapture(0) #start video...needs to move to client side.
        while(vid.isOpened()):
            img,frame = vid.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            client_socket.sendall(message)
            cv2.imshow('Sending...',frame)
            key = cv2.waitKey(10) 
            if key == 13:
                client_socket.close()