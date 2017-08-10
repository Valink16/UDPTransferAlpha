from myLib import *
import netifaces
from sys import getsizeof
from time import sleep,time
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
    interfaces=netifaces.interfaces()#Gets a list of available network interfaces

    for i,a in enumerate(interfaces):#Printing the list of interfaces(got the list from line 20)
        print("[{}]{}".format(i,a))
    print("")

    chInter=int(input("Chose an interface(enter the number): "))
    if(interfaces[chInter]=="lo"):
        ipBase="localhost"
    else:
        ipInfos=netifaces.ifaddresses(interfaces[chInter])#Gets all infos of local network from the chosen interface
        infos=ipInfos[netifaces.AF_INET]#Gets the ipv4 part
        ipBase=infos[0]["broadcast"][:11]#Gets broadcast from infos[0] dictionnary

    trgt=targtInfo(ipBase)
    continuer=True
    while(continuer):
        log(ipBase)
        with open(input("Name of the file to open: "),"rb") as file:
            sendFile=file.read()

        log("IP : {}".format(trgt[0]))
        log("PORT : {}".format(trgt[1]))
        log("Ready to communicate. Be sure that target is ready")
        s=0
        e=1024
        tStart=time()
        sChoice=int(input("Select speed:\n[0]:High speed\n[1]:Slow speed\n[2]:Very slow speed\n"))
        if(sChoice==0):
            waitTime=0.0003
        elif(sChoice==1):
            waitTime=0.001
        elif(sChoice==2):
            waitTime=0.01
        for i in range(1+(getsizeof(sendFile)//1024)):
            sender.sendto(sendFile[s:e],trgt)
            s+=1024
            e+=1024
            sleep(waitTime)

        print("Finished in {}s".format(time()-tStart))
        sender.sendto(b"stop",trgt)
        if(ask("Do you want to restart ?","Y","N")):
            continuer=True
        else:
            continuer=False
