from sys import getsizeof
from myLib import *
try:
    import socket
except:
    log("Failed to load socket")
    exit()

def recv():
    total=b""
    receiver=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    PORT=int(input("Enter receiver's port: "))
    receiver.bind(("",PORT))
    i=0
    while(True):
        recved, senderInfo=receiver.recvfrom(1024)
        print(getsizeof(recved))
        i+=1

        if recved.decode("utf-8")=="stop" or recved.decode("utf-8")=="exit" :
                break

        total+=recved

        print("Received {} bytes".format(len(total)))
    with open(input("Save as: "),"wb") as file:
        file.write(total)
