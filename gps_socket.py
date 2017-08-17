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



sock=None
STARTTIME=datetime.datetime.now()


DEBUG=False
#DEBUG=True
sock=None    #####  

# global variables:
gps_info={'fix':'0', 'course':0, 'speed':0,'altitude':0,
          'timex':'00:00:00 UTC',
          'XCoor':0,'YCoor':0,
          'LX':0,'LY':0,
          'dist':0.0}
#fix=None
#course=0#
#speed=0
#Alti=0
#timex="00:00:00 UTC"
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
    #global course,speed,XCoor, YCoor, Alti, timex
    global gps_info
    if (lin.find('GPRMC')>0):
#        if DEBUG: print("DEBUG", lin )
        gps_info['course']=lin.split(',')[8]
        gps_info['speed'] =lin.split(',')[7]
        try:
            gps_info['speed']=float(lin.split(',')[7])
        except:
            print('e... speed  ', end='\r')
            gps_info['speed']=0
        try:
            gps_info['course']=float(lin.split(',')[8])
        except:
            #print('e... course    ')
            gps_info['course']=0

    #-------- fix--------------------
def get_GPGSA(lin):
    global DEBUG
    global fix
    if (lin.find('GPGSA')>0):
        if (float(lin.split(',')[2])>1):
            gps_info['fix']='+'   #print( 'fix' )
            #if ( lin.find('GPGLL')>0):
            #    print('POSITION:')
        else:
            gps_info['fix']='!'
            #print('nofix')
        #return fix
    #else:
        #return None
    #----------------------------

#====== COORDINATES ============    
def get_GPGGA(lin ):
    global DEBUG
    #global course,speed,XCoor, YCoor, Alti, timex
    global gps_info
    if (lin.find('GPGGA')>0):
        tim=lin.split(',')[1]
        YCooS,XCooS=( lin.split(',')[2], lin.split(',')[4] )
        gps_info['altitude']= lin.split(',')[9]
        try:
            gps_info['altitude']=float( lin.split(',')[9])
        except:
            gps_info['altitude']=0
        try:
            XCoor1=floor(float(XCooS)/100.)
            XCoor=XCoor1+(float(XCooS)-XCoor1*100)/60.

            YCoor1=floor(float(YCooS)/100.)
            YCoor=YCoor1+(float(YCooS)-YCoor1*100)/60.
            if ( lin.split(',')[3]=="S"):
                YCoor=-YCoor
            if ( lin.split(',')[5]=="W"):
                XCoor=-XCoor
            gps_info['XCoor']=XCoor
            gps_info['YCoor']=YCoor
        except:
            print("e... error in division X Y Coor", end='\r')
            XCoor=0
            YCoor=0
        try:
            gps_info['timex']=tim[0:2]+':'+tim[2:4]+':'+tim[4:6]+' UTC'
        except:
            print("...error in timex")
            gps_info['timex']="00:00:00 UTC"
        #redraw=1  # HERE I DEFINE REDRAW
        #return Alti,XCoor,YCoor,timex


    

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

###################################
#
#
#
###################################
# X Y X Y
def get_dist_prec(lon2, lat2, lon1, lat1):
    if DEBUG: print(lon2, lat2, lon1, lat1)
#def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
#    print('converted to radians')
    return  c * r


###############################
#
#  LOOP
#
###############################
    

def translate_gps_line():
    global sock
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
            print('  USB:',aa[0],end="\n")
    #if data.find('WATCH'): # --- comm 3/ WATCH..many
        #print(' Watch.',end="")
    if DEBUG: print("DEBUG",data)
    if (data=="KILL"):  #------------- KILL SOCKET ----
        print( 'No data from socket')
        time.sleep(1)
        sock.close()
        sock=None
        gps_info['fix']="-"
    # --- data is here ----------------------        
    lin=data.rstrip()
    #lin=line.decode('utf-8').rstrip()
    #if DEBUG: print('LIN DEBUG',lin)
    ##################################################
    get_GPRMC(lin)
    if DEBUG: print("DEBUG","course speed ok",gps_info['course'],
                    gps_info['speed'])
    get_GPGSA(lin)
    if DEBUG: print("DEBUG","fix =",gps_info['fix'])
    get_GPGGA(lin)
    if DEBUG: print("DEBUG","X Y Coor ok",gps_info['XCoor'],
                    gps_info['YCoor'])
    # REDRAW HERE
    DELTA=datetime.datetime.now()-STARTTIME
    DELTA=str(DELTA)[:-7]
    #==
    gps_info['dist']=get_dist_prec(gps_info['XCoor'],
                                   gps_info['YCoor'],
                                   gps_info['LX'],
                                   gps_info['LY'] )
    if gps_info['dist']!=0.0:
        #print( "{:.5f}".format( 1000*gps_info['dist'])  )
        gps_info['LX']=gps_info['XCoor']
        gps_info['LY']=gps_info['YCoor']
#    try:
        #print("======= print all")
        # print(' '+gps_info['fix']+gps_info['timex']+
        #       " ({:6.4f},{:6.4f}){:6.1f} km/h {:6.1f} m H{:03.0f} {} {:.1f}     \r".format( gps_info['XCoor'],                                              gps_info['YCoor'],                                                    gps_info['speed']*1.852,                                              gps_info['altitude'],                                                 gps_info['course'], DELTA,
        #     gps_info['dist']*1000
        # ) ,end='\r')
 #   except:
#        print("=== not all values ready to print ======")
        ##sys.stdout.flush()


    
    return
