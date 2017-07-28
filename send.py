from myLib import *
try:
    import socket
except:
    log("Failed to load socket")
    exit()

def targtInfo():
    IP=input("Target IP : ")
    PORT=int(input("Target PORT : "))
    return (IP,PORT)
