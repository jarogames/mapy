#!/usr/bin/env python3
################ gpspipe 
#import subprocess
################# socket
#
#        EU   BIGCIT   smallCIT   streetS
#  zooms 5      8       12         15
#  EUROPE
# 5:   ./mkmap.pl 5 -15 65.2  5 5 > a.png
#   CZ
# 8:   ./mkmap.pl 8 10 51.2  7 4 > a.png                   [15:28:32]
# DE
# 8:   ./mkmap.pl 8 5 51.2  7 5 > a.png
# FR nord
#./mkmap.pl 8 -5 51.2  10 5 > a.png
# FR TOT
#./mkmap.pl 8 -5 51.2  10 11 > a.png
# EU
#./mkmap.pl 8 -5 51.2  20 15 > a.png
#12:  PRAGUE
#  ./mkmap.pl 12 14 50.2  8 4 > a.png
# CZ ALL 
#./mkmap.pl 12 12.30 51.1  73 46 > a.png
#SEVERNI FR
# ./mkmap.pl 12 -0.7 50.0 83 25  > a.png
#
#
zoomset=[5,8,12,15]

import socket
import sys
from math import sqrt, atan2
import datetime # for timer

DEBUG=False
#DEBUG=True


########################################### SOCKET FUNCTION #######################
#read one line from the socket
def buffered_readLine(socket):
    global DEBUG
    line = ""
    while True:
        try:
            part = str(socket.recv(1),'utf-8')
        except:
            part=""
#        print( '{'+part+'}' , len(part), len(line)  )
        if len(part)==0:
            return "KILL"
        if part != "\n":
            line=line+part
        elif part == "\n":
            break
    return line

#
import random
import time 
from math import floor,cos,sin

#######  MAIN THING - but my fork is necessary #####
from staticmap import StaticMap, CircleMarker, Line

############ i dont know
from IPython.core.display import Image, display
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


def get_dist(lon2, lat2, lon1, lat1):
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
    return floor( 10 *c * r)/10


def get_course( lon1, lat1, lon2, lat2):
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
#    rad=atan2(dlat*cos(lat2), dlon) / pi * 180
    rad=atan2(dlon*cos(lat2), dlat) / pi * 180
    if rad<0:
        rad=rad+360
    return int(rad)






def get_GPRMC(lin,c,s):
    global DEBUG
    if (lin.find('GPRMC')>0):
#        if DEBUG: print("DEBUG", lin )
        course=lin.split(',')[8]
        speed =lin.split(',')[7]
        try:
            speed=float(speed)
        except:
            speed=s
        try:
            course=float(course)
        except:
            course=c
        return course,speed
    else:
        return c,s

redraw=0
    #-------- fix--------------------
def get_GPGSA(lin,f):
    global DEBUG
    if (lin.find('GPGSA')>0):
        if (float(lin.split(',')[2])>1):
            fix='+' #print( 'fix' )
            #if ( lin.find('GPGLL')>0):
            #    print('POSITION:')
        else:
            fix='NOFIX'
        return fix
    else:
        return f
    #----------------------------
def get_GPGGA(lin,a,x,y,r):
    global DEBUG
    #print(fix)
    redraw=r
    if (lin.find('GPGGA')>0):
        tim=lin.split(',')[1]
        YCooS,XCooS=( lin.split(',')[2], lin.split(',')[4] )
        Alti= lin.split(',')[9]
        try:
            Alti=float(Alti)
        except:
            Alti=a
        try:
            XCoor1=floor(float(XCooS)/100.)
            XCoor=XCoor1+(float(XCooS)-XCoor1*100)/60.

            YCoor1=floor(float(YCooS)/100.)
            YCoor=YCoor1+(float(YCooS)-YCoor1*100)/60.
            if ( lin.split(',')[3]=="S"):
                YCoor=-YCoor
            if ( lin.split(',')[5]=="W"):
                XCoor=-XCoor
            redraw=1  # HERE I DEFINE REDRAW
        except:
            XCoor=x
            YCoor=y
        try:
            timex=tim[0:2]+':'+tim[2:4]+':'+tim[4:6]+' UTC'
        except:
            timex="00:00:00 UTC"
        #redraw=1  # HERE I DEFINE REDRAW
        return Alti,XCoor,YCoor,redraw,timex
    else:
        return a,x,y,r,"00:00:00 UTC"



    

def newwaypoint(WPOINT):
    global timex
    global dfT
    print('... newwaypoint',WPOINT)
    if options.target!=False:
        print(" going to open")
        with open(options.target+'.log', 'a') as f:
            print("opened and gonna write",timex)
            DELTA=datetime.datetime.now()-WPOINTIME
#            f.write('ahoj'+timex+'\n')
#            f.write(dfT.ix[WPOINT]['city'],',',dfT.ix[WPOINT]['y'],',',dfT.ix[WPOINT]['x'],',',timex)
            f.write( str(dfT.ix[WPOINT]['city'])+','+str(dfT.ix[WPOINT]['y'])+','+str(dfT.ix[WPOINT]['x'])+','+timex+','+DELTA+'\n')
        f.close()
    return WPOINT+1







################################################
#
#
#      INITIAL
#
##
##################################################

zoom=15
IMX=650*2
IMY=350*2


def gps_text(image,pos,text,fg='black',bg='white',radius=1.0):
    global DEBUG
    if DEBUG:print("DEBUG","entered gettext")
    global IMX
    global IMY
    draw = ImageDraw.Draw(image, 'RGBA')
    font22   = ImageFont.truetype("Ubuntu-B.ttf", 22)
    font14 = ImageFont.truetype("Ubuntu-B.ttf", 14)
    font=font22
    if isinstance(pos, str):
        font=font22
    else:
        font=font14
    w, h = draw.textsize(text, font)
    posi=(1,1)
    if DEBUG: print("DEBUG",'isinstantce str ')
    if isinstance(pos, str):
        if DEBUG: print('str ...', pos)
        if (pos=='lt'):
            posi=(1,1)
        if (pos=='lb'):
            posi=(1,IMY-h)
        if (pos=='rt'):
            posi=(IMX-w-2,1)
        if (pos=='rb'):
            posi=(IMX-w-2,IMY-h)
    else:
        if DEBUG: print("DEBUG",text,'course to ',pos)
        tox=IMX/2+sin(pos/180*pi)*IMX/2*radius
        toy=IMY/2-cos(pos/180*pi)*IMY/2*radius
        # shift the tox toy
        tox=int(tox-w/2)
        toy=int(toy-h/2)
        if (tox+w)>IMX: tox=IMX-w-1
        if (tox)<0:   tox=1
        if (toy+h/2)>=IMY: toy=IMY-h/2
        if (toy)<0:   toy=1
#        if ( sin(pos)>=0):
#            tox=tox-w
#        if (cos(pos)>0):
#            toy=toy-h
#        posi=( int(tox), int(toy) )
        posi=( tox, toy )
         
    if DEBUG: print('DEBUG','120=', w,h, posi, IMX,IMY)
    posf=( posi[0]+w , posi[1]+h )
    whitefog=(255, 255, 255, 110)
    blackfog=(0, 0, 0, 110)
    redfog=(255,0,0,  110)
    greenfog=(0,125,0,  110)
    white=(255,255,255)
    black=(0,0,0)
    red=(255,0,0)
    green=(0,255,0)
    ##### SPEED
    #text="{:4.1f}".format(speed*1.852)+' km/h'
    if fg=='black': fcol=black
    if fg=='white': fcol=white
    if fg=='red':   fcol=red
    if fg=='green': fcol=green
    if bg=='black': bcol=blackfog
    if bg=='white': bcol=whitefog
    if bg=='red':   bcol=redfog
    if bg=='green': bcol=greenfog
    draw.rectangle( [posi,posf] , bcol )
    draw.text( posi,text,         fcol , font=font)
    if DEBUG: print('DEBUG','rectg and text ok')



    

print("\n\n ./gpsmap3.py -x 620 -y 310 -z 15 -c CZ\n ./gpsmap3.py -x 1320 -y 710 -z 15 -c CZ ")
parser = OptionParser()

parser.add_option("-x", "--width", dest="IMX", type="int",
                  help="")
parser.add_option("-y", "--height", dest="IMY",type="int",
                  help="")
parser.add_option("-z", "--zoom", dest="zoom",type="int",
                  help="use zoom 11 and 15 only, 16,17,18 a.tile.osm")
#parser.add_option("-c", "--city", dest="city",action="store_true",
#                  default=False,  help="display city")
parser.add_option("-c", "--city", dest="city", 
                  default=False,  help="display city from country CZ,FR,DE,IT,FR100,DE100,IT100,CZ15,CZ100")
parser.add_option("-t", "--target", dest="target", 
                  default=False,  help="display target from file")
parser.add_option("-T", "--reverse_target", dest="targetrev", 
                  default=False,  help="display target from file")

parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()
print(options)
if options.IMX!=None: IMX=options.IMX
if options.IMY!=None: IMY=options.IMY
if options.zoom!=None: zoom=options.zoom

############################################### CITIES  CSV:
#http://download.geonames.org/export/dump/
# cat cities15000.txt | grep -i europe |  awk -F '\t' '{print $15",\""$2"\","$5","$6",_"$9"_"}' | sort -nr  > souradniceEU.csv
if options.city=="CZ":
    df1=pd.read_csv("souradnice2.csv",header=None)
    df1.columns=['city','y','x']
if options.city=="FR":
    df1=pd.read_csv("souradniceFR.csv",header=None)
    df1.columns=['people','city','y','x','c']
if options.city=="DE":
    df1=pd.read_csv("souradniceDE.csv",header=None)
    df1.columns=['people','city','y','x','c']
if options.city=="IT":
    df1=pd.read_csv("souradniceIT.csv",header=None)
    df1.columns=['people','city','y','x','c']

if options.city=="CZ100":
    df1=pd.read_csv("souradniceCZ100k.csv",header=None)
    df1.columns=['people','city','y','x','c']
if options.city=="CZ15":
    df1=pd.read_csv("souradniceCZ.csv",header=None)
    df1.columns=['people','city','y','x','c']
if options.city=="FR100":
    df1=pd.read_csv("souradniceFR100k.csv",header=None)
    df1.columns=['people','city','y','x','c']
if options.city=="DE100":
    df1=pd.read_csv("souradniceDE100k.csv",header=None)
    df1.columns=['people','city','y','x','c']
if options.city=="IT100":
    df1=pd.read_csv("souradniceIT100k.csv",header=None)
    df1.columns=['people','city','y','x','c']

dfT=None
WPOINT=0
WPOINTIME=datetime.datetime.now()
if options.targetrev!=False:
    options.target=options.targetrev
    print('REVERSED TARGET')
if options.target!=False:
    print("TARGET DEFINED", options.target)
    dfT=pd.read_csv( options.target ,header=None)
    dfT.columns=['city','y','x']
    print('NORMALORDER dfT',dfT)

if options.targetrev!=False:
    dfT=dfT.iloc[::-1]
    dfT=dfT.reset_index(drop=True)
    print('REVERSING dfT',dfT)


print(options.city)
print(IMX,IMY)
IMX,IMY=(int(IMX/2),int(IMY/2))


###### tinker stuff#############################################
root = tkinter.Tk()
label = tkinter.Label(root)
label.pack()
img = None
tkimg = [None]  # This, or something like it, is necessary because if you do not keep a reference to PhotoImage instances, they get garbage collected.
delay = 500   # in milliseconds
#img = Image.new('1', (100, 100), 0)




m1 = StaticMap( IMX,IMY, url_template='http://localhost:8900/{z}/{x}/{y}.png')

maxmarkers=4*25*2 ## because the forward arrow

redraw=0
once=0
XCoor,YCoor=(  14.9+0.00*random.random(), 50.0+0.00*random.random()  )
lastXY=(0,0)


#############
#
#   starting Popen OR SOCKET
#
#############
timex="00 00 00"
data="KILL"
speed=0
course=0
timex='00:00:00 UTC'
sock=None
redraw=0  # just sometimes switch off
fix="NOFIX"
cloproach=10000  # closest approach for WPOINT
################################################ LOOOOOOOOOOP ################
def loop():
    global dfT
    global df1
    global timex
    global fix
    global maxmarkers
    global tkimg
    global speed
    global course
    global timex
    global lastXY
    global sock
    global redraw
    global DEBUG
    global WPOINT
    global WPOINTIME
    global cloproach

####    course,speed=(0,0)
#    fix="NOFIX"
    Alti,XCoor,YCoor=(0, 14.9+0.003*random.random(), 50.+0.003*random.random()  )

    if (sock is None ):
        print('starting sock .... ',sock )
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 2947)
        print( 'connecting to %s port %s' % server_address)
        time.sleep(2)
        sock.connect(server_address)
        # Send data
        message = '?WATCH={"enable":true,"nmea":true}\n'
        #print( 'sending "%s"' % message)
        sock.sendall( str.encode(message) )
        print('WATCH sent', end='\r')
    data=""
#    print('DEBUG communicating sock .... ' )
    try:
        #time.sleep(1)
        if DEBUG: print("DEBUG tried sock")
        data=buffered_readLine(sock)
        ################################################ONE DATA
        #data=buffered_readLine(sock)
        #print('P{'+data+'}')
        #while (len(data)>0):
        if DEBUG: print("DEBUG",data)
        if (data=="KILL"):
            print( 'kill - closing socket - finally')
            time.sleep(2)
            sock.close()
            sock=None
            redraw=0
            fix="NOFIX"
            root.update_idletasks()
            root.after( 2, loop )
            return
            ###break
        #data=buffered_readLine(sock)
        lin=data.rstrip()
        #lin=line.decode('utf-8').rstrip()
        if DEBUG: print('LIN DEBUG',lin)
        ##################################################
        course,speed=get_GPRMC(lin,course,speed)
        if DEBUG: print("DEBUG","course speed ok",course,speed)
        #        redraw=0
        fix=get_GPGSA(lin,fix)
        if DEBUG: print("DEBUG","fix ok")
        Alti,XCoor,YCoor,redraw,timex=get_GPGGA(lin,Alti,XCoor,YCoor,redraw)
        if redraw==1:
            DELTA=datetime.datetime.now()-WPOINTIME
            print(' '+fix+timex+" {:6.4f} {:6.4f}/ {:4.1f} {:4.1f} {:4.1f} {}\r".format( XCoor,YCoor , speed, Alti, course, DELTA) ,end='\r')
            #sys.stdout.flush()
        if DEBUG: print('DEBUG redraw==', redraw)

        if (redraw==1):
            if DEBUG:print("DEBUG redraw==1 part of loop")
            mmaxm=maxmarkers
            if zoom<15:
                maxmarkers=(15-zoom)*maxmarkers
            if (abs(XCoor)<0.005 and abs(YCoor)<0.005):
                maxmarkers=2
            color='black'
            if fix=="+": color='red'
               
            mam= CircleMarker( (XCoor,YCoor), color, 6) 
            m1.add_marker(mam, maxmarkers=maxmarkers )
            if DEBUG: print("DEBUG",fix,"corrections")
            if fix=="+":  # first touch crashes
                if ( abs(YCoor)<90):
                    crf=cos(pi*YCoor/180)
                else:
                    crf=1.
                if DEBUG:print( "COOR==",XCoor, YCoor )
                lastXY=(XCoor, YCoor);

                r=0.002* (16-zoom)**1.8
                dx=r*sin(course/180*pi)/crf
                dy=r*cos(course/180*pi)
                if DEBUG:print("DEBUG {:.5f}  {:.5}  {:.5f}".format(dx,dy,r))
                mam= CircleMarker( (XCoor+dx,YCoor+dy), 'green', 9) 
                m1.add_marker(mam, maxmarkers=maxmarkers )
                mam= CircleMarker( (XCoor+dx*1.07,YCoor+dy*1.07), 'green', 6) 
                m1.add_marker(mam, maxmarkers=maxmarkers )
                mam= CircleMarker( (XCoor+dx*1.12,YCoor+dy*1.12), 'green', 4) 
                m1.add_marker(mam, maxmarkers=maxmarkers )
            if DEBUG: print("DEBUG", "m11 render ")
            mapproblem=0
            try:
                image=m1.render(zoom=zoom, center=(XCoor,YCoor))
            except:
                print('maps with zoom=',zoom,'not found')
                mapproblem=1
            if mapproblem>0:
                mapproblem=0
                try:
                    image=m1.render(zoom=12)
                except:
                    mapproblem=1
                    print('maps with zoom=',12,'not found')
            if mapproblem>0:
                mapproblem=0
                try:
                    image=m1.render(zoom=8)
                except:
                    mapproblem=1
                    print('maps with zoom=',8,'not found')
            if mapproblem>0:
                mapproblem=0
                try:
                    image=m1.render(zoom=5)
                except:
                    mapproblem=1
                    print('maps with zoom=',5,'not found')
            m1.remove_last_marker()
            m1.remove_last_marker()
            m1.remove_last_marker()
            if DEBUG: print("DEBUG", "i want to draw now")
            draw = ImageDraw.Draw(image, 'RGBA')
            font   = ImageFont.truetype("Ubuntu-B.ttf", 22)
            font16 = ImageFont.truetype("Ubuntu-B.ttf", 16)
            ##### SPEED
            gps_text(image,'lt',"{:4.1f}".format(speed*1.852)+' km/h')
            ##### HEADING
            gps_text(image,'rt',"{:3.0f}".format(course))
            ##### Altitude
            gps_text(image,'lb',"{:5.0f} m".format(Alti))
            ##### TIME
            gps_text(image,'rb',timex)
                
            if options.city and not(df1 is  None):
                if DEBUG: print('------------------------ on id')
                #print(df1)
                if ( abs(YCoor)<90):
                    crf=cos(pi*YCoor/180)

                i=(   (df1['y']-YCoor)**2+((df1['x']-XCoor)*crf)**2 ).argsort()[0]
                #print(crf,'crf',i,'i')
                idi=get_dist(XCoor,YCoor,df1.ix[i]['x'],df1.ix[i]['y'] )
                rad=1.
                if idi<0.5: rad=idi*2
                #print(crf,'crf',i,'i', 'idi===',idi)
                cour=get_course(XCoor,YCoor,df1.ix[i]['x'],df1.ix[i]['y'])
                #print('course',cour)
                gps_text(image,cour,"{} {} ".format(df1.ix[i]['city'],idi),fg='white', bg='black',radius=rad)

                i=(   (df1['y']-YCoor)**2+((df1['x']-XCoor)*crf)**2 ).argsort()[1]
                #print(crf,'crf',i,'i')
                idi=get_dist(XCoor,YCoor,df1.ix[i]['x'],df1.ix[i]['y'] )
                rad=1.0
                if idi<0.5: rad=idi*2
                #print(crf,'crf',i,'i', 'idi===',idi)
                cour=get_course(XCoor,YCoor,df1.ix[i]['x'],df1.ix[i]['y'])
                #print('course',cour)
                gps_text(image,cour,"{} {} ".format(df1.ix[i]['city'],idi),fg='white', bg='black',radius=rad)

                i=(   (df1['y']-YCoor)**2+((df1['x']-XCoor)*crf)**2 ).argsort()[2]
                #print(crf,'crf',i,'i')
                idi=get_dist(XCoor,YCoor,df1.ix[i]['x'],df1.ix[i]['y'] )
                rad=1.
                if idi<0.5: rad=idi*2
                #print(crf,'crf',i,'i', 'idi===',idi)
                cour=get_course(XCoor,YCoor,df1.ix[i]['x'],df1.ix[i]['y'])
                #print('course',cour)
                gps_text(image,cour,"{} {} ".format(df1.ix[i]['city'],idi),fg='white', bg='black',radius=rad)
############################################################ NAVIGATION ########################                
            ######################################### DFT   -1 == LAST POSSIBLE WAYPOINT always there
            if ( abs(YCoor)<90):
                crf=cos(pi*YCoor/180)
            if options.target and not(dfT is  None) and len(dfT)>1:
                if DEBUG:print('------------------------ on TGT -1')
                i=len(dfT)-1
                if DEBUG:print(crf,'-1Tcrf',i,'i')
                idi=get_dist(XCoor,YCoor,dfT.ix[i]['x'],dfT.ix[i]['y'] )
                if DEBUG:print(crf,'-1Tcrf',i,'=i', 'idi===',idi)
                cour=get_course(XCoor,YCoor,dfT.ix[i]['x'],dfT.ix[i]['y'])
                if DEBUG:print('-1Tcourse',cour)
                rad=1.0
                if idi<0.5:rad=idi*2
                gps_text(image,cour,"{} {} ".format(dfT.ix[i]['city'],idi),fg='white',bg='green',radius=rad)
            ######################################### DFT  WPOINT == 1st/WPOINT(th) ON NEXT WAYPOINT
            # 2 modes:  not clear what to use
            #   1/when closer than 0.5km, NEXT;  /strict waypooint check/
            #   2/OR when the next is closer,    /rather intentional waypoints/
            #   1b/ closest approach +-1km...
            #
            if options.target and not(dfT is  None) and (len(dfT)>WPOINT):
                
                if DEBUG:print('------------------------ on TGT WPOINT')
                WPOINT=(   (dfT['y']-YCoor)**2+((dfT['x']-XCoor)*crf)**2 ).argsort()[0]
                i=WPOINT
                if DEBUG:print('WPOINT==',WPOINT,i,'==i', dfT.ix[i]['city'])
                idi=get_dist(XCoor,YCoor,dfT.ix[i]['x'],dfT.ix[i]['y'] )
                if DEBUG:print(crf,'Tcrf',i,'=i', 'idi===',idi)
                cour=get_course(XCoor,YCoor,dfT.ix[i]['x'],dfT.ix[i]['y'])
                if DEBUG:print('Tcourse',cour)
                rad=0.8
                if idi<0.5:
                    rad=idi*2
                gps_text(image,cour,"{} {} ".format(dfT.ix[i]['city'],idi),fg='white',bg='red',radius=rad)
                #WPOINT=newwaypoint(WPOINT) # WPOINT=WPOINT+1 # I WANT WRITE HERE
                ########### switch to new WPOINT
                if idi<0.9:
                    if  (idi>cloproach):
                        WPOINT=newwaypoint(WPOINT) # WPOINT=WPOINT+1 # I WANT WRITE HERE
                        DELTA=datetime.datetime.now()-WPOINTIME
                        print("NEW WAYPOINT ON CLOSETS APPROACH", WPOINT, cloproach, DELTA)
                        WPOINTIME=datetime.datetime.now()
                        cloproach=10000.
                        idi=10000
                        for ai in range(WPOINT-1,-1,-1):
                            dfT.set_value( ai, 'x', 0)
                            dfT.set_value( ai, 'y', 0)
#                ######### else just keep cloproach minimum
                if idi<cloproach:
                    cloproach=idi ## refresh last value
                    print('cloproach decreased {:5.1f} km    '.format( idi) )
                ### in case of missed target or sleeping gps: ###################
                if (len(dfT)>=WPOINT):
#                    if DEBUG:print('searching idi2','WP==',i,WPOINT)
#                    idi2=get_dist(XCoor,YCoor, dfT.ix[i+1]['x'],dfT.ix[i+1]['y'] )
#                    print("IDI 2 is ",idi2,'IDI1 = ',idi)
#                    if idi2<idi:
#                        WPOINT=WPOINT+1
#                        print("NEW WAYPOINT BY HALF DISTANCE", WPOINT, idi, idi2)
                    if idi>cloproach*1.5:
#                        WPOINT=WPOINT+1
                        print("NEW WAYPOINT BY 150% CLOSEST APPROACH", WPOINT, idi, cloproach)
                        cloproach=10000.
                        idi=10000
                        WPOINT=WPOINT+1
                        for ai in range(WPOINT-1,-1,-1):
                            dfT.set_value( ai, 'x', 0)
                            dfT.set_value( ai, 'y', 0)
                        
#################################################################################################                 

            image=image.resize( (IMX*2,IMY*2) )
            #image.save('map.png')
            tkimg[0] = ImageTk.PhotoImage(image)
            label.config(image=tkimg[0])
            #root.update_idletasks()
            #root.after( 20, loop )
            #time.sleep(0.1)
            mam= CircleMarker( (XCoor,YCoor),  'orange', 6) 
            m1.add_marker( mam, maxmarkers=maxmarkers )
#            lastXY=(XCoor, YCoor);
            redraw=0
        ####### here i am after redraw.    
            maxmarkers=mmaxm
            if DEBUG: print('DEBUG endofloop')


        ################################################ONE DATA
    except:
        print("SOCKET CRASH")
        time.sleep(2)
        sock.close()
        sock=None
        redraw=0
        fix="NOFIX"

        
                ###################################################
    root.update_idletasks()
    root.after( 2, loop )


#neve happens
loop()
#task.wait()
root.mainloop()

