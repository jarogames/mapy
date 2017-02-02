#!/usr/bin/env python3
import subprocess
import pandas as pd
import random
import time 
from math import floor
from staticmap import StaticMap, CircleMarker, Line
from IPython.core.display import Image, display
import numpy


# from PIL import Image
# from PIL import ImageFont
# from PIL import ImageDraw 
# # feh --reload 0.3 map.png
# root = Tk.Tk()
# label = Tk.Label( root )
# label.pack()



zoom=15
IMX=650
IMY=350
m1 = StaticMap( IMX,IMY, url_template='http://localhost:8900/{z}/{x}/{y}.png',fixzoom=zoom)
#mam=[]
maxmarkers=25

redraw=1
once=0
#while True:

#    print( xbin[ix], ybin[iy] )
XCoor,YCoor=(  0+0.003*random.random(), 0+0.003*random.random()  )



#df = pd.DataFrame()
task = subprocess.Popen(["/bin/sh",'-c', " stdbuf -i0 -o0  -e0 gpspipe -r"], stdout=subprocess.PIPE)
fix=''
for line in task.stdout:
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
        except:
            XCooS=0.
            YCooS=0.
            XCoor,YCoor=(0 +0.004*random.random(),0+0.004*random.random())

        print( fix, tim[0:2]+':'+tim[2:4]+':'+tim[4:8],'UTC {:6.5f} {:6.5f}'.format( XCoor,YCoor ), speed, Alti, course )
        redraw=1
        
    
    if (redraw==1):
        mmaxm=maxmarkers
        if (abs(XCoor)<0.005 and abs(YCoor)<0.005):
            maxmarkers=2
        color='black'
        if fix=="+": color='red'
        mam= CircleMarker( (XCoor,YCoor), color, 5) 
        m1.add_marker(mam, maxmarkers=maxmarkers )
        image=m1.render()

        draw = ImageDraw.Draw(image, 'RGBA')
        font = ImageFont.truetype("Ubuntu-B.ttf", 22)
        draw.rectangle( [(30, 5),(120,30)] ,  (0, 0, 0, 80)  )
        draw.text((30, 5),"{:.1f}".format(speed)+' km/h',(124,252,0), font=font)
        
        draw.rectangle( [(20, IMY-22),(120,IMY)] ,  (0, 0, 0, 80)  )
        draw.text((20, IMY-22),str(Alti)+' m',(255,255,255), font=font)

        draw.rectangle( [(IMX-100, 5),(IMX,30)] ,  (0, 0, 0, 80)  )
        draw.text((IMX-100, 5),str(course)+' deg',(255,255,255), font=font)

        image=image.resize( (IMX*2,IMY*2) )
#        print( type(image))
        #if yrng%10:
        image.save('map.png')
        ##display( image )
        if once==0: image.show()
        once=once+1
        time.sleep(0.1)
        mam= CircleMarker( (XCoor,YCoor),  'orange', 5) 
        m1.add_marker( mam, maxmarkers=maxmarkers )
#        print(len(mam))
        redraw=0
        maxmarkers=mmaxm

#    else:
#        print("NOT",lin)
task.wait()
