import socket
import SpringDB_Requests as requests
import SpringDB as DB
import threading
import json
import subprocess
#import PLEXAPI as papi
host = '127.0.0.1'  #127 == local, use wlan ip for non local connection     Static ip = 192.168.1.1
port = 5571         #any port is fine, just make sure both parties know it
DB = DB.DataBase()



jsonFormat = {"part_id" : 0,         #id for the type of part being made
              "work_id": 0,          #id of the workstation being used
              "job_id": 0,           #id for the job being performed
              "part_len": 0.0,       #length of the part being made aka how much raw material is used
              "part_type": "",       #type of part being made
              "part_capacity": 100}  #how many parts the job requires to be made




def setup_server():
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

    connection, address = socket.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    t = threading.Thread(target=data_transfer,args=(connection,address[0]))
    t.start()
    setup_connection(socket)


def PROCESS(data):
    requests.new_data(data)


def data_transfer(conn,ip):

    # A big loop that sends/receives data until told not to.
    while True:
        # Try to Receive the data coming from connection
        try:
            data = conn.recv(1024)  # receive the data
        except:
            #if it recieves nothing or an exit from connection the will close connection on this side
            print("connection closed")
            conn.close
            exit()

        data = data.decode("utf-8")


        #set up msg from leaf would be    setup;workstationID
        if len(data) > 5:
            if data[0:5] == 'setup':
                setup(conn,ip,data[6:])



        try:
            conn.sendall(json.dumps(data).encode("utf-8"))
        except Exception as ex:
            print("connection closed due to \n" + str(ex))
            conn.close
            exit()
    conn.close()

def setup(conn,ip,workcenter):
    wheel_diam = "0.0"
    if DB.workcenter_addr_to_id(ip) != None:
        #Ask trevor how to update DB
        #DB.update("workcenters",ip,)
        workcenter = DB.get("workcenters",ip)
        wheel_diam = workcenter[3]
    else:
        msg = "INVALID"
        msg.encode("utf-8")
        conn.sendall(msg)
        setup(conn,ip,workcenter)


    msg = "wheel_diam:" + wheel_diam
    msg.encode("utf-8")
    conn.sendall(msg)

    if wheel_diam == "0.0":
        buf = conn.recv(1024)
        buf.decode("utf-8")
        wheel_diam = buf[7:]
        #DB.update("workcenters",ip)





"""
Calls SprindDB method to get the entire workcenter table, from this we can ping all ip addresses
on record, and attach a workcenter to them. This will help people know if a leaf is offline

It works by using a subprocess of the ping command. Sends 1 packet and if it times out, assumes no leaf is offline.
"""
def pingAllIPs():
    rows = DB.get_all("workcenters")
    for x in rows[0]:
        ip = x[0]
        param = '-n '
        command = ['ping',param,'1',ip]
        if (subprocess.call(command) == 0):
            print("true")
        else:
            print("cant connect to ip: " + x[0])




s = setup_server()
