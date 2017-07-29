from myLib import *
from time import sleep

#This is a test. It could be integrated to the original TCP transfer program.
S=True
R=False
mode=ask("Send or receive a file?(S/R)\n","S","R")#We are making the send and receive part in the same file, unlike the TCP transfer program.
print(mode)
if(mode==S):
    log("User chose send\n")
    from send import *
    send()
elif(mode==R):
    log("User chose receive")
    from recv import *
    recv()
