from myLib import *
try:
    import socket
except:
    log("Failed to load socket")
    exit()

def recv():
    receiver=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    PORT=int(input("Enter receiver's port: "))
    receiver.bind(("",PORT))
    while(True):
        recved, senderInfo=receiver.recvfrom(1024)
        print(recved.decode("utf-8"))
        if(recved.decode("utf-8")=="stop" or recved.decode("utf-8")=="exit"):
            break
