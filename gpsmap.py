#!/usr/bin/env python3
import subprocess
import pandas as pd
import random
import time 
from staticmap import StaticMap, CircleMarker, Line
from IPython.core.display import Image, display
import numpy

zoom=15

m1 = StaticMap(500,300, url_template='http://localhost:8900/{z}/{x}/{y}.png',fixzoom=zoom)

maxmarkers=9

#while True:

#    print( xbin[ix], ybin[iy] )



#df = pd.DataFrame()
task = subprocess.Popen(["/bin/sh",'-c', "gpspipe -r"], stdout=subprocess.PIPE)
fix=''
for line in task.stdout:
    lin=line.decode('utf-8').rstrip()
    if (lin.find('GPGSA')>0):
        if (float(lin.split(',')[2])>1):
            fix=''#print( 'fix' )
            if ( lin.find('GPGLL')>0):
                print('POSITION:')
        else:
            fix=' NOFIX'
#    if (lin.find('GPGGA')>0):
#        tim=lin.split(',')[1]
#        print( fix, tim[0:2]+':'+tim[2:4]+':'+tim[4:8],' UTC' )#df=pd.concat(
    if (lin.find('GPGLL')>0):
        tim=lin.split(',')[5]
        print( fix, tim[0:2]+':'+tim[2:4]+':'+tim[4:8],' UTC' )#df=pd.concat(
        XCoor,YCoor=( lin.split(',')[1], lin.split(',')[3] )
        ###########   case FIX IS OK ###########
        if (fix==""):
            XCoor1=floor(float(XCoor)/100.)
            XCoor=XCoor1+(float(XCoor)-XCoor1*100)/60.

            YCoor1=floor(float(YCoor)/100.)
            YCoor=YCoor1+(float(YCoor)-YCoor1*100)/60.

            if ( lin.split(',')[1]=="S"):
                YCoor=-YCoor
                if ( lin.split(',')[1]=="E"):
                    XCoor=-XCoor
        print(lin,' pos:', XCoor,YCoor )

    XCoor,YCoor=(  14.238+0.003*random.random(), 49.864 +0.003*random.random()  )
    mam=CircleMarker( (XCoor,YCoor),  'red', 5)
    m1.add_marker(mam, maxmarkers=maxmarkers )
    image=m1.render()
    image=image.resize( (1000,600) )
    #if yrng%10:
    image.save('map.png')
    ##display( image )
    ##image.show()
    time.sleep(0.9)
    mam=CircleMarker( (XCoor,YCoor),  'blue', 5)
    m1.add_marker( mam, maxmarkers=maxmarkers )

#    else:
#        print("NOT",lin)
task.wait()
