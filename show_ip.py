from grove_rgb_lcd import *
import socket

def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    print(s.getsockname()[0])
    ip = s.getsockname()[0]
    s.close()
    return ip


ip = getIp()

setText("My IP:\n" + ip)

#setText("Czesc michale")
