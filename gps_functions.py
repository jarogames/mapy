def get_dist(lon2, lat2, lon1, lat1):
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
    return floor( 10 *c * r)/10

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




#
    #-------- fix--------------------
def get_GPGSA(lin,f):
    global DEBUG
    global fix
    if (lin.find('GPGSA')>0):
        if (float(lin.split(',')[2])>1):
            fix='+' #print( 'fix' )
            #if ( lin.find('GPGLL')>0):
            #    print('POSITION:')
        else:
            fix='NOFIX'
            #print('nofix')
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

#
def newwaypoint(WPOINT, WPOINTLEN):
    global timex
    global dfT
    global m1
    global options
    print('... newwaypoint {}  {:5.2f} km            '.format(WPOINT,WPOINTLEN))
    if options.target!=False:
        #print(" going to open")
        with open(options.target+'.log', 'a') as f:
            print("opened and gonna write",datetime.datetime.now())
            DELTA=datetime.datetime.now()-WPOINTIME
            DELTA=str(DELTA)[:-7]
            WPL="{:5.1f} km".format(WPOINTLEN)
            f.write( str(dfT.ix[WPOINT]['city'])+','+str(dfT.ix[WPOINT]['y'])+','+str(dfT.ix[WPOINT]['x'])+','+str(datetime.datetime.now())[:-7]+','+str(DELTA)+','+str(WPL)+'\n')
            f.close()

    print('... newwAFTEROP {}  {:5.2f} km            '.format(WPOINT,WPOINTLEN))
    if not(dfT is None) and (len(dfT)<=WPOINT+1):
        #if DEBUG:
        print('========== Returning same END WPOINT', WPOINT,'len=',len(dfT))
        return WPOINT
    else:
        if not m1 is None:
            for ii in range(WPOINT,-1,-1):
                if not dfT is None:
                    mam = CircleMarker( ( dfT.ix[ii]['x'],dfT.ix[ii]['y'] ), 'lightgrey', 9)
                    m1.add_marker( mam )
                    dfT.set_value( ii, 'x' , 0)
                    dfT.set_value( ii, 'y' , 0)
    
    print("....returning ",WPOINT,WPOINT+1)
    return WPOINT+1

