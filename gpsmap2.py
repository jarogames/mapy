#!/usr/bin/env python3
import subprocess
import pandas as pd
import random
import time 
from math import floor
from staticmap import StaticMap, CircleMarker, Line
from IPython.core.display import Image, display
import numpy


from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import tkinter
from PIL import Image, ImageTk



from optparse import OptionParser

zoom=18
IMX=650
IMY=350

parser = OptionParser()

parser.add_option("-x", "--width", dest="IMX", type="int",
                  help="")
parser.add_option("-y", "--height", dest="IMY",type="int",
                  help="")
parser.add_option("-z", "--zoom", dest="zoom",type="int",
                  help="")

parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()
print(options)
if options.IMX!=None: IMX=options.IMX
if options.IMY!=None: IMY=options.IMY
if options.zoom!=None: zoom=options.zoom
print(IMX,IMY)

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
            course=None
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
            Alti="{:5.1f}".format(Alti)
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
        timex=tim[0:2]+':'+tim[2:4]+':'+tim[4:8]+' UTC'
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

        if (fix=="+"):
            dx=XCoor-lastXY[0]
            dy=YCoor-lastXY[1]
#            print('last', (lastXY[0],lastXY[1]), 'white', 5 )
#            mam= CircleMarker( (lastXY[0],lastXY[1]), 'white', 5) 
#            m1.add_marker(mam, maxmarkers=maxmarkers )

#            print(  (XCoor+dx*14,YCoor+dy*14), 'white', 3 )
            mam= CircleMarker( (XCoor+dx*maxmarkers,YCoor+dy*maxmarkers), 'magenta', 1) 
            m1.add_marker(mam, maxmarkers=maxmarkers )
        print('goint to render',fix)
        image=m1.render()

        draw = ImageDraw.Draw(image, 'RGBA')
        font = ImageFont.truetype("Ubuntu-B.ttf", 22)
        draw.rectangle( [(5, 5),(120,30)] ,  (255, 255, 255, 120)  )
        draw.text((5, 5),"{:.1f}".format(speed*1.852)+' km/h',(0,0,0), font=font)

        draw.rectangle( [(5, IMY-22),(120,IMY)] ,  (0, 0, 0, 80)  )
        draw.text((5, IMY-22),str(Alti)+' m',(255,255,255), font=font)

        draw.rectangle( [(IMX-125, 5),(IMX,30)] ,  (0, 0, 0, 80)  )
        draw.text((IMX-125, 5),str(course)+' dg',(255,255,255), font=font)

        draw.rectangle( [(IMX-155, IMY-22),(IMX,IMY)] ,  (0, 0, 0, 80)  )
        draw.text((IMX-155, IMY-22), timex ,(255,255,255), font=font)

        image=image.resize( (IMX*2,IMY*2) )
        image.save('map.png')
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

