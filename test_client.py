import socket
import json

import time #incase you want to use time.sleep
host = '127.0.0.1' #IP address of Pi
port = 5571

#creates connection to seerver
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


s.sendall(b"Sending")              #this sendall is for testing purposes


data = b''                         #a byte sting aka a string that can read bytes


recvBuffer = s.recv(2048)          #the raw encoded bytes being send across socket


data += recvBuffer                 #adds the recieved bytes to the byte string
data = json.loads(data.decode())   #decodes the bytes and then serializes it back so it can be read as a dictionary



print(data['part_capacity'])       #making sure the dictionary works


#ends connection to the server
s.shutdown(socket.SHUT_RDWR)
s.close()
