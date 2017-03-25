#!/usr/bin/env python3

import socket
import sys
from math import sqrt, atan2
import datetime # for timer
### 2nd
import random
import time 
from math import floor,cos,sin
##
import re ### device from devices

#######  MAIN THING - but my fork is necessary #####
from staticmap import StaticMap, CircleMarker, Line

#from IPython.core.display import Image, display
import numpy
### PIL for printing on png file
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

################ TK to display
import tkinter
from PIL import Image, ImageTk

################ very nice options parser
from optparse import OptionParser

############### read .csv and search for vilages
import pandas as pd
from math import sqrt,cos,pi,floor,asin,radians

###################################################
#
# GLOBAL VARIABLES
#
###################################################
STARTTIME=datetime.datetime.now()


DEBUG=False
#DEBUG=True
sock=None    #####  

# global variables:
fix=None
course=0
speed=0
Alti=0
timex="00:00:00 UTC"
########################################### SOCKET FUNCTION #######################
#read one line from the socket
def buffered_readLine(socket):
    global DEBUG
    line = ""
    while True:
        try:
            part = str(socket.recv(1),'utf-8')
        except:
            return "KILL"#        print( '{'+part+'}' , len(part), len(line)  )
        if len(part)==0:
            return "KILL"
        if part != "\n":
            line=line+part
        elif part == "\n":
            break
    return line


def get_GPRMC(lin):
    global DEBUG
    global course,speed,XCoor, YCoor, Alti, timex
    if (lin.find('GPRMC')>0):
#        if DEBUG: print("DEBUG", lin )
        course=lin.split(',')[8]
        speed =lin.split(',')[7]
        try:
            speed=float(speed)
        except:
            speed=0
        try:
            course=float(course)
        except:
            course=0

    #-------- fix--------------------
def get_GPGSA(lin):
    global DEBUG
    global fix
    if (lin.find('GPGSA')>0):
        if (float(lin.split(',')[2])>1):
            fix='+'   #print( 'fix' )
            #if ( lin.find('GPGLL')>0):
            #    print('POSITION:')
        else:
            fix='!'
            #print('nofix')
        return fix
    else:
        return None
    #----------------------------

#====== COORDINATES ============    
def get_GPGGA(lin ):
    global DEBUG
    global course,speed,XCoor, YCoor, Alti, timex
    if (lin.find('GPGGA')>0):
        tim=lin.split(',')[1]
        YCooS,XCooS=( lin.split(',')[2], lin.split(',')[4] )
        Alti= lin.split(',')[9]
        try:
            Alti=float(Alti)
        except:
            print("...error in Alti")
            Alti=0
        try:
            XCoor1=floor(float(XCooS)/100.)
            XCoor=XCoor1+(float(XCooS)-XCoor1*100)/60.

            YCoor1=floor(float(YCooS)/100.)
            YCoor=YCoor1+(float(YCooS)-YCoor1*100)/60.
            if ( lin.split(',')[3]=="S"):
                YCoor=-YCoor
            if ( lin.split(',')[5]=="W"):
                XCoor=-XCoor
        except:
            print("...error in division X Y Coor")
            XCoor=0
            YCoor=0
        try:
            timex=tim[0:2]+':'+tim[2:4]+':'+tim[4:6]+' UTC'
        except:
            print("...error in timex")
            timex="00:00:00 UTC"
        #redraw=1  # HERE I DEFINE REDRAW
        return Alti,XCoor,YCoor,timex


    

#######################################################
#
#  SOCKET PART
#
#######################################################

# --- if no socket => create one --------------------
def getsock():
    global sock
    if (sock is None ):
        print('###################### NEW socket ... ',end="")
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 2947)
        print( '  {:s}:{:d} ...'.format(server_address[0],server_address[1]),end="")
        time.sleep(1)
        sock.connect(server_address)
        # Send data
        message = '?WATCH={"enable":true,"nmea":true}\n'
        sock.sendall( str.encode(message) )
        print('WATCH sent', end='\n')
        return sock


###############################
#
#  LOOP
#
###############################
    
for i in range(151):
#    print(i,"/" , end="\r" )
    getsock()    
    # --- clear data and read -----------------------------    
    data=""

    if DEBUG: print("DEBUG tried sock")
    data=buffered_readLine(sock)
    if data.find('VERSION'):  # --- communication 1/version
        aa=re.findall(r'"release":"(.+?)"',data)
        #if aa:
            #print('rel:',aa[0],end="")
        #print('Version')
    if data.find('DEVICES'):  # ---- comm 2/ devices !
        aa=re.findall(r'"path":"(.+?)"',data)
        if aa:
            print(' USB:',aa[0],end="\n")
    #if data.find('WATCH'): # --- comm 3/ WATCH..many
        #print(' Watch.',end="")
    if DEBUG: print("DEBUG",data)
    if (data=="KILL"):  #------------- KILL SOCKET ----
        print( 'No data from socket')
        time.sleep(1)
        sock.close()
        sock=None
        fix="NOFIX"
    # --- data is here ----------------------        
    lin=data.rstrip()
    #lin=line.decode('utf-8').rstrip()
    #if DEBUG: print('LIN DEBUG',lin)
    ##################################################
    get_GPRMC(lin)
    if DEBUG: print("DEBUG","course speed ok",course,speed)
    get_GPGSA(lin)
    if DEBUG: print("DEBUG","fix =",fix)
    get_GPGGA(lin)
    # REDRAW HERE
    try:
        #print("======= print all")
        DELTA=datetime.datetime.now()-STARTTIME
        DELTA=str(DELTA)[:-7]
        print(' '+fix+timex+" ({:6.4f},{:6.4f}){:6.1f} km/h {:5.1f} m H{:03.0f} {}        \r".format( XCoor,YCoor , speed*1.852, Alti, course, DELTA) ,end='\r')
    except:
        print("=== not all values ready to print ======")
        #sys.stdout.flush()
##############
#
#
#
##############



