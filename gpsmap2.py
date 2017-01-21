#!/usr/bin/env python3
##### gpspipe 
import subprocess
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


zoom=18
IMX=650*2
IMY=350*2

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


###### tinker stuff
root = tkinter.Tk()
label = tkinter.Label(root)
label.pack()
img = None
tkimg = [None]  # This, or something like it, is necessary because if you do not keep a reference to PhotoImage instances, they get garbage collected.
delay = 500   # in milliseconds
#img = Image.new('1', (100, 100), 0)

m1 = StaticMap( IMX,IMY, url_template='http://localhost:8900/{z}/{x}/{y}.png',fixzoom=zoom)

maxmarkers=25*2 ## because the forward arrow

redraw=1
once=0
XCoor,YCoor=(  0+0.003*random.random(), 0+0.003*random.random()  )
lastXY=(0,0)

task = subprocess.Popen(["/bin/sh",'-c', " stdbuf -i0 -o0  -e0 gpspipe -r"], stdout=subprocess.PIPE)
fix=''
speed=0
course=0
timex='00:00:00 UTC'
def loop():
    global fix
    global maxmarkers
    global tkimg
    global speed
    global course
    global timex
    global lastXY
    line=task.stdout.readline()
    #print('ITER',line)
    lin=line.decode('utf-8').rstrip()
    redraw=0
    if (lin.find('GPRMC')>0):
        course=lin.split(',')[8]
        speed =lin.split(',')[7]
        try:
            speed=float(speed)
        except:
            speed=0.
        try:
            course=float(course)
        except:
            course=0.0
    #-------- fix--------------------
    if (lin.find('GPGSA')>0):
        if (float(lin.split(',')[2])>1):
            fix='+' #print( 'fix' )
            #if ( lin.find('GPGLL')>0):
            #    print('POSITION:')
        else:
            fix=' NOFIX'
    #print(fix)        
    if (lin.find('GPGGA')>0):
        tim=lin.split(',')[1]
        YCooS,XCooS=( lin.split(',')[2], lin.split(',')[4] )
        Alti= lin.split(',')[9]
        try:
            Alti=float(Alti)
            #Alti="{:5.1f}".format(Alti)
        except:
            Alti=0.
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
            XCooS=0.
            YCooS=0.
            XCoor,YCoor=(0 +0.004*random.random(),0+0.004*random.random())
        timex=tim[0:2]+':'+tim[2:4]+':'+tim[4:6]+' UTC'
        print( fix, timex+' {:6.5f} {:6.5f}'.format( XCoor,YCoor ), speed, Alti, course )
        redraw=1  # HERE I DEFINE REDRAW

    #print('with', lin , ' redraw' )
    # i save number of markers 
    if (redraw==1):
        mmaxm=maxmarkers
        if (abs(XCoor)<0.005 and abs(YCoor)<0.005):
            maxmarkers=2
        color='black'
        if fix=="+": color='red'

        mam= CircleMarker( (XCoor,YCoor), color, 5) 
        m1.add_marker(mam, maxmarkers=maxmarkers )
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
                print("")
            dx=XCoor-lastXY[0]
            dy=YCoor-lastXY[1]
            mam= CircleMarker( (XCoor+dx*maxmarkers/2,YCoor+dy*maxmarkers/2), 'magenta', 1) 
            m1.add_marker(mam, maxmarkers=maxmarkers )
        image=m1.render()

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
                print('city error')

        image=image.resize( (IMX*2,IMY*2) )
        #image.save('map.png')
        tkimg[0] = ImageTk.PhotoImage(image)
        label.config(image=tkimg[0])

        time.sleep(0.1)
        mam= CircleMarker( (XCoor,YCoor),  'orange', 5) 
        m1.add_marker( mam, maxmarkers=maxmarkers )
        lastXY=(XCoor, YCoor);

        redraw=0
        maxmarkers=mmaxm
        #print('endofloop')
    root.update_idletasks()
    root.after( 10, loop )
    #root.mainloop() # should run in separate thread

#neve happens
loop()
#task.wait()
root.mainloop()

