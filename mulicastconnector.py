import socket
import threading
import time
UDP_IP = "192.168.1.255"
UDP_PORT = 8081

class connectionMan:
    cast = True
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    connections = []
    def __init__(self, obj):
        self.data = obj
        t = threading.Thread(target=self.recCast)
        t.start()
        print("Searching Sensor")
        self.sendCast()
        print("found")
    def sendCast(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
        while self.cast:
            s.sendto(b"c", (UDP_IP, UDP_PORT))
            time.sleep(0.5)
        s.close()
    def recCast(self):
        # Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set some options to make it multicast-friendly
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except AttributeError:
            pass # Some systems don't support SO_REUSEPORT
        s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
        s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

        # Bind to the port
        s.bind(('', UDP_PORT))
        count=0
        while True:
            data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
            #print(data.decode(), addr)
            if(data):
                if (data.decode() == "cd"):
                    print(addr[0], " connected")
                    self.connections.append(addr[0])
                    self.cast = False
                elif(data.decode()[0]=='m'):
                    self.cast = False
                    count+=1
                    #print("message:" ,int(data.decode()[1:]) )
                    self.data.add(count,int(data.decode()[1:]))
                else:
                    pass
        s.close()      
