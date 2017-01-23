#!/usr/bin/env  python3

import socket
import sys
import time

#read one line from the socket
def buffered_readLine(socket):
    line = ""
    while True:
        part = str(socket.recv(1),'utf-8')
#        print( '{'+part+'}' , len(part), len(line)  )
        if len(part)==0:
            return "KILL"
        if part != "\n":
            line=line+part
        elif part == "\n":
            break
    return line
data="KILL"
while (data=="KILL"):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 2947)
    print( 'connecting to %s port %s' % server_address)
    time.sleep(2)
    sock.connect(server_address)

    try:
        # Send data
        message = '?WATCH={"enable":true,"nmea":true}\n'
        print( 'sending "%s"' % message)
        sock.sendall( str.encode(message) )
        print('sent')
        data=buffered_readLine(sock)
        while (len(data)>0):
            print(data)
            if (data=="KILL"):
                break
            data=buffered_readLine(sock)

    finally:
        print( 'closing socket')
        time.sleep(2)
        sock.close()
