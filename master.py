import time
import socket
import os
import sys
#part 1
    
s=socket.socket()
host=socket.gethostname()
print(host)
port=5050 
s.bind((host,port))
print("")
print("Waiting for any incomming connections.............")
print("")
s.listen(1)
conn, addr=s.accept()
print(addr,"has connected to the server")
print("")
#part 2

command=input(str("command: "))
conn.send(command.encode())
print("command has been sent. Waiting for a confirmation")
data=conn.recv(1024)
if data:
    print("Command has benn recieved and has been executed")