from myLib import *
import netifaces
try:
    import socket
except:
    log("Failed to load socket")
    exit()

def targtInfo(baseIP):
    if(baseIP=="localhost"):
        print("IP: {}".format(baseIP))
        PORT=int(input("Target PORT : "))
        return (baseIP, PORT)
    IP=baseIP+input("Target IP : {}".format(baseIP))
    PORT=int(input("Target PORT : "))
    return (IP,PORT)

def send():
    sender=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    interfaces=netifaces.interfaces()

    with open("sample.txt","rb") as file:
        sendFile=file.read()
    for i,a in enumerate(interfaces):
        print("[{}]{}".format(i,a))
    print("")



    chInter=int(input("Chose an interface(enter the number): "))
    if(interfaces[chInter]=="lo"):
        ipBase="localhost"
    else:
        ipInfos=netifaces.ifaddresses(interfaces[chInter])
        infos=ipInfos[netifaces.AF_INET]
        ipBase=infos[0]["broadcast"][:11]

    log(ipBase)
    trgt=targtInfo(ipBase)
    log("IP : {}".format(trgt[0]))
    log("PORT : {}".format(trgt[1]))
    log("Ready to communicate. Be sure that target is ready")

    while(True):
        msg=input().encode("utf-8")
        sender.sendto(msg,trgt)
        if(msg==b"exit" or msg==b"stop"):
            break
