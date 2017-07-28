from myLib import *
from time import sleep
import subprocess
#This is a test. It could be integrated to the original TCP transfer program.
S=True
R=False
mode=ask("Send or receive a file?(S/R)\n","S","R")#We are making the send and receive part in the same file, unlike the TCP transfer program.
print(mode)
if(mode==S):
    log("User chose send")
    from send import *
    sender=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    trgt=targtInfo()
    log("Target's IP: {}".format(trgt[0]))
    log("Target's PORT: {}".format(trgt[1]))
    log("Ready to communicate. Be sure that target is ready")
    while(True):
        msg=input().encode("utf-8")
        if(msg==b"exit" or msg==b"stop"):
            break
        sender.sendto(msg,trgt)
        
elif(mode==R):
    log("User chose receive")
    from recv import *

