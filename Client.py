# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 17:10:27 2022

@author: pirit
"""

import socket
import sys
from time import sleep

#HOST = "localhost"
#HOST = "127.0.0.1"
HOST = '192.168.56.1'
#HOST = "LAPTOP-MHPGQ8F5"
# HOST = "::1"
# The server's hostname or IP address
# The IP address 127.0.0.1 is the standard IPv4 address for the loopback interface
PORT = 2500
# The port used by the server
# port represents the TCP port number to accept connections on from clients

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #    #socket.socket() creates a socket object
    # No need to call s.close()
    # AF_INET is the Internet address family for IPv4
    # SOCK_STREAM is the socket type for TCP
    s.connect((HOST, PORT))
    # It creates a socket object, uses .connect() to connect to the server
    data = s.recv(1024).decode("utf-8")
    print(data)
    
    while True:
        print("Yo: ", end='')
        msg = input("")
        
        if msg == 'salir':
            sys.exit()

        elif msg == '3':
            state = s.recv(1024).decode("utf-8")
            while 'Estamos' in state:

            
                
        elif msg =='4':
            s.sendall(msg.encode())
            data = s.recv(1024).decode("utf-8")
            print(data)
            sleep(5)
            sys.exit()
        else:
            s.sendall(msg.encode())
            data = s.recv(1024).decode("utf-8")
            print(data)
        
        
