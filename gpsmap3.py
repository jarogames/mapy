#!/usr/bin/env python3
################ gpspipe 
#import subprocess
################# socket
import socket
import sys
from math import sqrt
DEBUG=False
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
#http://download.geonames.org/export/dump/
# cat cities15000.txt | grep -i europe |  awk -F '\t' '{print $15",\""$2"\","$5","$6",_"$9"_"}' | sort -nr  > souradniceEU.csv
#
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
    return floor( 10 *c * r)/10
#    print('-------getdist:',lon2, lat2, lon1, lat1)
#    R = 6378  #// radius of the earth in km
#    x = (lon2 - lon1)/180*pi* cos( 0.5*(lat2+lat1) /180*pi)
#    y = (lat2 - lat1)/180*pi
#    d = R * sqrt( x*x + y*y )
#    return floor(d*10)/10







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

parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()
print(options)
if options.IMX!=None: IMX=options.IMX
if options.IMY!=None: IMY=options.IMY
if options.zoom!=None: zoom=options.zoom

if options.city=="CZ":
    df1=pd.read_csv("souradnice2.csv")
    df1.columns=['city','y','x']
if options.city=="FR":
    df1=pd.read_csv("souradniceFR.csv")
    df1.columns=['people','city','y','x','c']
if options.city=="DE":
    df1=pd.read_csv("souradniceDE.csv")
    df1.columns=['people','city','y','x','c']
if options.city=="IT":
    df1=pd.read_csv("souradniceIT.csv")
    df1.columns=['people','city','y','x','c']

if options.city=="CZ100":
    df1=pd.read_csv("souradniceCZ100k.csv")
    df1.columns=['people','city','y','x','c']
if options.city=="CZ15":
    df1=pd.read_csv("souradniceCZ.csv")
    df1.columns=['people','city','y','x','c']
if options.city=="FR100":
    df1=pd.read_csv("souradniceFR100k.csv")
    df1.columns=['people','city','y','x','c']
if options.city=="DE100":
    df1=pd.read_csv("souradniceDE100k.csv")
    df1.columns=['people','city','y','x','c']
if options.city=="IT100":
    df1=pd.read_csv("souradniceIT100k.csv")
    df1.columns=['people','city','y','x','c']


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

m1 = StaticMap( IMX,IMY, url_template='http://localhost:8900/{z}/{x}/{y}.png',fixzoom=zoom)

maxmarkers=25*2 ## because the forward arrow

redraw=0
once=0
XCoor,YCoor=(  14.9+0.00*random.random(), 50.0+0.00*random.random()  )
lastXY=(0,0)


#############
#
#   starting Popen OR SOCKET
#
#############

data="KILL"

#task = subprocess.Popen(["/bin/sh",'-c', " stdbuf -i0 -o0  -e0 gpspipe -r"], stdout=subprocess.PIPE)





fix='NOFIX'
speed=0
course=0
timex='00:00:00 UTC'
sock=None
redraw=0  # just sometimes switch off
fix="NOFIX"
def loop():
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
        print( 'sending "%s"' % message)
        sock.sendall( str.encode(message) )
        print('sent')
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
            print( fix, timex+' {:6.5f} {:6.5f}'.format( XCoor,YCoor ), speed, Alti, course )
        if DEBUG: print('DEBUG redraw==', redraw)

        if (redraw==1):
            print("DEBUG redraw==1 part of loop")
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
                try:
                    #print( 'correction cos',YCoor/180,cos(pi*YCoor/180) )
                    crf=cos(pi*YCoor/180)
                    #                print( 'correction cos',cos(YCoor/180*pi) )
                    i=(   (df1['y']-YCoor)**2+((df1['x']-XCoor)*crf)**2 ).argsort()[0] 
                    j=(   (df1['y']-YCoor)**2+((df1['x']-XCoor)*crf)**2 ).argsort()[1] 
                    k=(   (df1['y']-YCoor)**2+((df1['x']-XCoor)*crf)**2 ).argsort()[2]
                    idi=get_dist(XCoor,YCoor,df1.ix[i]['x'],df1.ix[i]['y'] )
                    idj=get_dist(XCoor,YCoor,df1.ix[j]['x'],df1.ix[j]['y'] )
                    idk=get_dist(XCoor,YCoor,df1.ix[k]['x'],df1.ix[k]['y'] )
                except:
                    crf=0;print("pandas ijk badly")
                dx=XCoor-lastXY[0]
                dy=YCoor-lastXY[1]
                r=sqrt(dx*dx*crf*crf+dy*dy)
                dx=dx/r  *0.0001/2 # ok for 15
                dy=dy/r * 0.0001/2
                mam= CircleMarker( (XCoor+dx*maxmarkers/2,YCoor+dy*maxmarkers/2), 'magenta', 5) 
                m1.add_marker(mam, maxmarkers=maxmarkers )
            if DEBUG: print("DEBUG", "m11 render ")
            image=m1.render()
            m1.remove_last_marker()
            if DEBUG: print("DEBUG", "i want to draw now")
            draw = ImageDraw.Draw(image, 'RGBA')
            font   = ImageFont.truetype("Ubuntu-B.ttf", 22)
            font16 = ImageFont.truetype("Ubuntu-B.ttf", 16)
            ##### SPEED
            draw.rectangle( [(5, 5),(120,30)] ,  (255, 255, 255, 120)  )
            draw.text((5, 5),"{:4.1f}".format(speed*1.852)+' km/h',(0,0,0), font=font)
            ##### HEADING
            draw.rectangle( [(IMX-50, 0),(IMX,30)] ,  (0, 0, 0, 80)  )
            draw.text((IMX-50, 0),"{:3.0f}".format(course),(255,255,255), font=font)
            ##### Altitude
            draw.rectangle( [(0, IMY-20),(90,IMY)] ,  (0, 0, 0, 80)  )
            draw.text((0, IMY-22),"{:5.0f} m".format(Alti),(255,255,255), font=font)
            ##### TIME
            draw.rectangle( [(IMX-140, IMY-20),(IMX,IMY)] ,  (0, 0, 0, 80)  )
            draw.text((IMX-140, IMY-22), timex ,(255,255,255), font=font)
            
            ##### position
            if (options.city):
                try:
                    draw.rectangle( [(0, IMY-40),(IMX,IMY-24)] ,  (0, 0, 0, 80)  )
                    draw.text((0, IMY-42), "{} {},     {} {},    {} {}".format(df1.ix[i]['city'],idi,df1.ix[j]['city'],idj,df1.ix[k]['city'],idk),(255,255,255), font=font16)
                except:
                    #print('DEBUG city error')
                    abcd=1
                    
            image=image.resize( (IMX*2,IMY*2) )
            #image.save('map.png')
            tkimg[0] = ImageTk.PhotoImage(image)
            label.config(image=tkimg[0])
            #root.update_idletasks()
            #root.after( 20, loop )
            #time.sleep(0.1)
            mam= CircleMarker( (XCoor,YCoor),  'orange', 5) 
            m1.add_marker( mam, maxmarkers=maxmarkers )
            lastXY=(XCoor, YCoor);
            redraw=0
        ####### here i am after redraw.    
            maxmarkers=mmaxm
            print('DEBUG endofloop')


        ################################################ONE DATA
    except:
        print("SOCKET CRASH")
        time.sleep(2)
        sock.close()
        sock=None
        redraw=0
        fix="NOFIX"

        
                ###################################################
#    finally:
#        #root.update_idletasks()
#        print( 'closing socket - finally')
#        time.sleep(2)
#        sock.close()
#        sock=None
#    print('DEBUG ending loop with data')
    root.update_idletasks()
    root.after( 2, loop )

    #if data!="KILL":
    #    return
   
    #line=task.stdout.readline()
    #print('ITER',line)
    #lin=line.decode('utf-8').rstrip()

    #print('with', lin , ' redraw' )
    # i save number of markers 

    #root.mainloop() # should run in separate thread

#neve happens
loop()
#task.wait()
root.mainloop()

