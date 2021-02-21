import socket

host = '127.0.0.1' #IP address of Pi
port = 5571

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    cmd = input("Enter Command: ")
    if cmd == 'EXIT':
        s.send(str.encode(cmd))
        break
    elif cmd == 'KILL':
        s.send(str.encode(cmd))
        break
    s.send(str.encode(cmd))
    reply = s.recv(1024)
    print(reply.decode('utf-8'))

s.close()

