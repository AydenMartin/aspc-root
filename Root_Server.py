import socket

host = ''
port = 5560
n_connections = 1
storedReply = ''
def ServerSetup():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(host, port)
    except socket.error as msg:
        none = None
        #Dosomething

    return s
def GET():
    reply = storedReply
    return reply

def REPEAT(data):
    reply = data[1]
    return reply

def InitializeConnection():
    s.listen(n_connections)
    connection, address = s.accept()
    return connection

def DataTransfer(connection):
    while True:
        data = connection.recv(1024)
        data = data.decode("utf-8")
        #Parse and process recieved data
        message = data.split(' ', 1)
        cmd = message[0]
        if cmd == 'GET':
            reply = GET()
        elif cmd == 'REPEAT':
            reply = REPEAT(message)
        elif cmd == 'EXIT':
            break
        elif cmd == 'KILL':
            s.close();
            break
        else:
            reply = 'Unkn'

        connection.sendall(str.encode(reply))

s = ServerSetup()
while True:
    try:
        connection = ServerSetup()
        DataTransfer(connection)
    except:
        break
