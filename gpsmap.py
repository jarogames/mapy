#!/usr/bin/env python3
import subprocess
import pandas as pd
import random
import time 
from math import floor
from staticmap import StaticMap, CircleMarker, Line
from IPython.core.display import Image, display
import numpy

# feh --reload 0.3 map.png

zoom=15

m1 = StaticMap(650,350, url_template='http://localhost:8900/{z}/{x}/{y}.png',fixzoom=zoom)
#mam=[]
maxmarkers=25

redraw=1
#while True:

#    print( xbin[ix], ybin[iy] )
XCoor,YCoor=(  0+0.003*random.random(), 0+0.003*random.random()  )



#df = pd.DataFrame()
task = subprocess.Popen(["/bin/sh",'-c', " stdbuf -i0 -o0  -e0 gpspipe -r"], stdout=subprocess.PIPE)
fix=''
for line in task.stdout:
    lin=line.decode('utf-8').rstrip()
    redraw=0
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
        if (len(XCooS)<4): XCooS="0"
        if (len(YCooS)<4): YCooS="0"
        XCoor,YCoor=(0 +0.004*random.random(),0+0.004*random.random())
        ###########   case FIX IS OK ###########
        if (fix=="+"):
            XCoor1=floor(float(XCooS)/100.)
            XCoor=XCoor1+(float(XCooS)-XCoor1*100)/60.

            YCoor1=floor(float(YCooS)/100.)
            YCoor=YCoor1+(float(YCooS)-YCoor1*100)/60.
            if ( lin.split(',')[3]=="S"):
                YCoor=-YCoor
            if ( lin.split(',')[5]=="W"):
                XCoor=-XCoor

        print( fix, tim[0:2]+':'+tim[2:4]+':'+tim[4:8],'UTC {:6.5f} {:6.5f}'.format( XCoor,YCoor ) )
        redraw=1
        
    # if (lin.find('GPGLL')>0):
    #     redraw=1
    #     tim=lin.split(',')[5]
    #     print( fix, tim[0:2]+':'+tim[2:4]+':'+tim[4:8],' UTC' )#df=pd.concat(
    #     YCoor,XCoor=( lin.split(',')[1], lin.split(',')[3] )
    #     ###########   case FIX IS OK ###########
    #     if (fix==""):
    #         XCoor1=floor(float(XCoor)/100.)
    #         XCoor=XCoor1+(float(XCoor)-XCoor1*100)/60.

    #         YCoor1=floor(float(YCoor)/100.)
    #         YCoor=YCoor1+(float(YCoor)-YCoor1*100)/60.

    #         if ( lin.split(',')[1]=="S"):
    #             YCoor=-YCoor
    #         if ( lin.split(',')[3]=="W"):
    #             XCoor=-XCoor
    #     else:
    #         XCoor,YCoor=(  14.238+0.003*random.random(), 49.864 +0.003*random.random()  )
    #     print(lin,' pos:', XCoor,YCoor )

    if (redraw==1):
        mmaxm=maxmarkers
        if (abs(XCoor)<0.005 and abs(YCoor)<0.005):
            maxmarkers=2
        color='black'
        if fix=="+": color='red'
        mam= CircleMarker( (XCoor,YCoor), color, 5) 
        m1.add_marker(mam, maxmarkers=maxmarkers )
        image=m1.render()
        image=image.resize( (1300,700) )
        #if yrng%10:
        image.save('map.png')
        ##display( image )
        ##image.show()
        time.sleep(0.1)
        mam= CircleMarker( (XCoor,YCoor),  'orange', 5) 
        m1.add_marker( mam, maxmarkers=maxmarkers )
#        print(len(mam))
        redraw=0
        maxmarkers=mmaxm

#    else:
#        print("NOT",lin)
task.wait()
