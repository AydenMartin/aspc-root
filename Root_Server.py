import socket
import SpringDB_Requests as requests
host = '127.0.0.1'
port = 5571

def setup_server():
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        sckt.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    return sckt


def setup_connection():
    s.listen(1)  # Allows one connection at a time.
    connection, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return connection


def PROCESS(data):
    requests.new_data(data)


def data_transfer(conn):
    # A big loop that sends/receives data until told not to.
    while True:
        # Receive the data
        data = conn.recv(1024)  # receive the data
        data = data.decode('utf-8')
        # Split the data such that you separate the command
        # from the rest of the data.
        dataMessage = data.split(':', 1)
        command = dataMessage[0]
        if command == 'EXIT':
            break
        elif command == 'KILL':
            s.close()
            break
        elif command == 'PUT':
            PROCESS(data)
            reply = 'Command Received'
        else:
            reply = 'Unable to process'
        conn.sendall(str.encode(reply))
    conn.close()


s = setup_server()

while True:
    try:
        conn = setup_connection()
        data_transfer(conn)
    except:
        break