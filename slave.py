import time
import socket
import os
import sys

#part 1 complete
s=socket.socket()
host="DESKTOP-4U0ASN6"
port=5050 
s.connect((host, port))
print("connected to server")
#part2
command=s.recv(1024)
command=command.decode()
#part3
if command=="shutdown":
    print("Shutdown is bieng executed")
    s.send("Command recieved".encode())
    os.system("shutdown.bat")    