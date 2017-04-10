#!/usr/bin/env python3
from gps_socket import translate_gp_line, gps_info
from staticmap import StaticMap, CircleMarker, Line

###############################
#
#  LOOP
#
###############################
IMX=320
IMY=240
resizeF=2
m1 = StaticMap( IMX,IMY, url_template='http://localhost:8900/{z}/{x}/{y}.png')

for i in range(9999999):
    translate_gp_line()
    #print(i,"    ",gps_info['timex']  )
    #image=m1.render(zoom=8,center=(gps_info['XCoor'],gps_info['YCoor']) )
    if gps_info['fix']=='+' and gps_info['dist']>0.:
        mam= CircleMarker( (gps_info['XCoor'],gps_info['YCoor']),'red', 1)
        m1.add_marker(mam)
        image=m1.render(zoom=15,
                        center=(gps_info['XCoor'],gps_info['YCoor'])  )
        image=image.resize( (int(IMX* resizeF) , int(IMY*resizeF) ) )
        #print('save')
        image.save('map.png')
##############
#
#
#
##############



