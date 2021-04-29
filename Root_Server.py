import socket
import SpringDB_Requests as requests
import threading
import json
host = '127.0.0.1'  #127 == local, use wlan ip for non local connection
port = 5571         #any port is fine, just make sure both parties know it



jsonFormat = {"part_id" : 0,         #id for the type of part being made
              "work_id": 0,          #id of the workstation being used
              "job_id": 0,           #id for the job being performed
              "part_len": 0.0,       #length of the part being made aka how much raw material is used
              "part_type": "",       #type of part being made
              "part_capacity": 100}  #how many parts the job requires to be made




def setup_server():
    """
    Initialize server

    :return: None
    """
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        sckt.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    sckt.listen(10)
    setup_connection(sckt)


def setup_connection(socket):
    """
    Sets up a connection with a given socket

    :return: None
    """
    connection, address = socket.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    t = threading.Thread(target=data_transfer,args=(connection,))
    t.start()
    setup_connection(socket)

def data_transfer(conn):
    """
    Continuously listen for communication from sensors

    :return: None
    """
    # A big loop that sends/receives data until told not to.
    while True:
        # Receive the data
        #time.sleep(2)
        try:
            data = conn.recv(1024)  # receive the data
        except:
            print("connection closed")
            conn.close
            exit()

        print(data.decode("utf-8"))

        try:
            conn.sendall(json.dumps(jsonFormat).encode("utf-8"))
        except Exception as ex:
            print("connection closed due to \n" + str(ex))
            conn.close
            exit()

    conn.close()


s = setup_server()
