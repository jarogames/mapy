#!/usr/bin/env python3
#%matplotlib inline
#pbf  http://download.geofabrik.de/europe.html
#https://switch2osm.org/serving-tiles/building-a-tile-server-from-packages/
# localy http://a.tile.osm.org/3/4/2.png
# http://a.tile.komoot.de/komoot-2/3/4/2.png
#feh --reload 0.3 map.png
# for ((i=0;i<100;i++)); do echo map.jpg; done | xargs  mpv -speed=0.8
#
# downloadosmtiles --lat=49:51 --lon=13:16 --zoom=15
#find $dir -size 0 -exec rm  {} \;

import time 
from staticmap import StaticMap, CircleMarker, Line
from IPython.core.display import Image, display
import numpy

zoom=15

degpertile={ 6:5.625,7:2.813, 8:1.406, 9:0.703, 10:0.352, 11:0.176, 12:0.088, 13:0.044, 14:0.022, 15:0.011 }
mperpixel={ 6:2444,7:1222, 8:610.98, 9:305.492, 10:152.746, 11:76.373, 12:38.187, 13:19.093, 14:9.547, 15:4.773 }
#print( degpertile[15] )

bieville=[49.085, -0.891, ]
oustiup=[  49.361, -0.8123 ]   # oustriham

lowfr=[48.5198017, -2.0462775]
hipils=[49.8198353, 12.5435664] # pilsen

#CATANIA
fontanarosa=[37.3944531, 14.9002194]
accireale=[37.6455161, 15.1856494]

#PARIS
SArnould=[48.5600361, 1.9313314]
ReezFosseM=[49.0970392, 2.9104878]
#stred cz 15
xl=14.099
yl=49.80
xh=14.76
yh=50.27

#### caen 15
xl=bieville[1]
yl=bieville[0]
xh=oustiup[1]
yh=oustiup[0]

###  frcz  11 
#xl=lowfr[1]
#yl=lowfr[0]
#xh=hipils[1]
#yh=hipils[0]

zoom=15  # CATANIA
xl=fontanarosa[1]
yl=fontanarosa[0]
xh=accireale[1]
yh=accireale[0]

zoom=15  # PARIS
xl=SArnould[1]
yl=SArnould[0]
xh=ReezFosseM[1]
yh=ReezFosseM[0]



xbin=numpy.linspace( xl, xh,  (xh-xl)/degpertile[zoom] )
ybin=numpy.linspace( yl, yh, (xh-xl)/degpertile[zoom] )
totalm=0
for ix in range(len(xbin)-1):
    for iy in range(len(ybin)-1):
        totalm=totalm+1
        print( totalm,'.',xbin[ix], ybin[iy],  degpertile[15])
        
m1 = StaticMap(256, 256, url_template='http://localhost:8900/{z}/{x}/{y}.png',fixzoom=zoom)
Step=0.006
maxmar=1
total=0
for ix in range(len(xbin)-1):
    for iy in range(len(ybin)-1):
        total=total+1
        print( total,'/',totalm,'.',xbin[ix], ybin[iy] )
        XCoor,YCoor=(  xbin[ix], ybin[iy]  )
        mam=CircleMarker( (XCoor,YCoor),  'red', 5)
        m1.add_marker(mam, maxmarkers=maxmar )
        image=m1.render()
        #image=image.resize( (1000,600) )
        #if yrng%10:
        image.save('map.png')
        ##display( image )
        ##image.show()
        ##time.sleep(0.1)
#        mam=CircleMarker( (XCoor,YCoor),  'blue', 5)
#        m1.add_marker( mam, maxmarkers=maxmar )


