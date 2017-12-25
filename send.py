from myLib import *
import netifaces, platform
from sys import getsizeof
from time import sleep,time

try:
	import winreg
except:
	log("Not importing winreg")
try:
    import socket
except:
    log("Failed to load socket")
    exit()

def targtInfo(baseIP, limitedMode=False):

    if baseIP=="localhost" or limitedMode:
        print("IP: {}".format(baseIP))
        PORT=int(input("Target PORT : "))
        return (baseIP, PORT)

    IP=baseIP+input("Target IP : {}".format(baseIP))
    PORT=int(input("Target PORT : "))
    return (IP,PORT)

def guidTranslate(guid):
    """
    Function to "translate" GUID that windows returns to "netifaces.interfaces() into a readable String"
    GUID Example:  {9D69D2C8-4528-42A1-8B07-D102A79F463F}
    Function source: https://stackoverflow.com/questions/29913516/how-to-get-meaningful-network-interface-names-instead-of-guids-with-netifaces-un
    """
    localReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    regKey = winreg.OpenKey(localReg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
    
    try:    
        regSubkey = winreg.OpenKey(regKey, guid + r"\Connection")
        return winreg.QueryValueEx(regSubkey, "Name")[0]
    except FileNotFoundError:
        return -1 # if can't translate


def send():

    packetSize=1024

    OS = platform.system()
    sender=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    interfaces=netifaces.interfaces()#Gets a list of available network interfaces

    while(True): #Loop until a correct interface is choosen
        for i,a in enumerate(interfaces):#Printing the list of interfaces
            if OS == "Windows":
                name = guidTranslate(a) #See guidTranslate function declaration for informations.
                if name == -1:
                    name = a # If cannot translate, let it as it was
            else:    
                name = a #Other OSs than Windows don't need to translate to print "readable" names
            print("[{}]{}".format(i,name))
        print("")

        chInter=int(input("Chose an interface(enter the number): "))
        
        try:
            if(interfaces[chInter]=="lo"): #Only works on POSIX/Linux
                ipBase="localhost"
            else:
                ipInfos=netifaces.ifaddresses(interfaces[chInter])#Gets all infos of local network from the chosen interface
                infos=ipInfos[netifaces.AF_INET]#Gets the ipv4 part
                ipBase=infos[0]["broadcast"][:11]#Gets broadcast from infos[0] dictionnary
                trgt=targtInfo(ipBase, False)
                break
        
        except KeyError: # Windows raises KeyError for some network interfaces
            log("Your chosen interface cannot be used.")
            ipBase = input("Manually enter IP or enter 'r' to choose an other interface: ")
            if not ipBase.upper() == "R":
                trgt=targtInfo(ipBase, True)
                break

        
    
    continuer=True
    while(continuer):
        log(ipBase)
        with open(input("Name of the file to open: "),"rb") as file:
            sendFile=file.read()

        log("IP : {}".format(trgt[0]))
        log("PORT : {}".format(trgt[1]))

        sChoice=int(input("Select speed:\n[0]:High speed\n[1]:Slow speed\n[2]:Very slow speed\n"))
        if(sChoice==0):
            waitTime=0.0003
        elif(sChoice==1):
            waitTime=0.001
        elif(sChoice==2):
            waitTime=0.01

        log("Ready to communicate. Be sure that target is ready")

        s=0
        e=packetSize
        tStart=time()
        
        for i in range(1+(getsizeof(sendFile)//1024)):
            sender.sendto(sendFile[s:e],trgt)
            s+=packetSize
            e+=packetSize
            sleep(waitTime)

        print("Finished in {}s".format(time()-tStart))
        sender.sendto(b"stop",trgt)

        if(ask("Do you want to restart ?","Y","N")):
            continuer=True
        else:
            continuer=False
