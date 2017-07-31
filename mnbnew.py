#!/usr/bin/env python3
from gps_socket import translate_gp_line, gps_info
#  gps_info  -   directory:  fix,course,altitude,timex,XCoor,YCoor,LX,LY (=lastXY),dist
#  install last staticmap
#pip3 install --user git+git://github.com/komoot/staticmap@master --upgrade #
#
# downloadosmtiles --baseurl=http://localhost:8900 --lat=43:46.1  --lon=8.48:12.7 --zoom=12

#
from staticmap import StaticMap, CircleMarker, Line
#============
import threading
import time
import zmq
import pickle
import subprocess
#  try gpsmon for checking...
###############################
#
#  LOOP
#
###############################
def monitor_size():
    CMD="xrandr  | grep \* | cut -d' ' -f4"
    p=subprocess.check_output(CMD , shell=True)
    wihe=p.decode('utf8').rstrip().split('x')
    wihe=list(map(int,wihe))
    return wihe

IMX=320
IMY=240

#IMX=640
#IMY=480
IMX,IMY=monitor_size()
resizeF=2
IMX=int(IMX/resizeF)-20
IMY=int(IMY/resizeF)-20
m1 = StaticMap( IMX,IMY, url_template='http://localhost:8900/{z}/{x}/{y}.png')
zoomset=[5,8,15]   # zoom  0,1,2
zoom=15
zoom=8
zoom=5
##### 0 1 2 - it parses allowed zoomset
zoom=3



### asi by mela byt nejaka hlavni fronta, ktera sbira commandy
def keydown(e):
    global m1
    print('keypressed')
    if len(e.char)==0: return 
    print('     keypress /'+e.char+'/')
    if e.char==' ':
        print('SPACE')
    if e.char in ['q']:
        print('should be QUITTING...')
        ##quit()
    return

################################## 
#     MOUSE 
#
def callback(event):
    global m1
    frame.focus_set()
    print( "clicked at", event.x, event.y,"  ")
    print( m1._x_to_lon(m1._px_to_x(), zoom ) )


label=None
root=None

def loop(context=None):
    global zoom
    global label
    global root
    from PIL import ImageTk
    time.sleep(0.01)
    #print( gps_info['XCoor'],gps_info['YCoor']  )
    #print( gps_info['XCoor'],gps_info['YCoor']  )

    #context = context or zmq.Context.instance()
    #context =  zmq.Context()
    # 
    #receivertki = context.socket(zmq.SUB)
    #####receivertki.connect("inproc://workertki")
    #receivertki.connect("tcp://localhost::56543")
    #print('looTKI: ... ... waiting from master ')
    #string = receivertki.recv()
    #print('looTKI: ... ... GOT from master ')
    #context.term()
    #mam= CircleMarker( ( 14.5 , 50.0 ), 'blue', 10) # praha
    #mam= CircleMarker( ( 49.0 , 14.0 ), 'blue', 10) # middle east
    mam= CircleMarker(  (gps_info['XCoor'] , gps_info['YCoor'] ), 'blue', 4)
    m1.add_marker( mam )
    while len(m1.markers)>20:
        m1.markers.pop(0)
    #print( 'MARKERS=', len(m1.markers) )
    for z in range( zoom,-1,-1):
        try:
            image=m1.render(zoom=zoomset[z] , center=(gps_info['XCoor'] , gps_info['YCoor'] )   )
            #print('GOOD ZOOM',z,  end="\r")
            if zoom!=z:
                print('NEW ZOOM=', z, 'old = ', zoom)
                zoom=z
            break
        except:
            print('BAD ZOOM',z, end='\r')
                
    image=image.resize( (int(IMX* resizeF) , int(IMY*resizeF) ) )

    tkimg = ImageTk.PhotoImage(image)
    label.config(image=tkimg)
    root.update_idletasks()
    root.after( 2, loop )
    time.sleep( 0.5 )  # sleep here to leave it displayed
    


def worker_tki(context=None):
    '''
    The first worker I did= it just displays the text line on the screen
    '''
    import tkinter
    from PIL import Image, ImageTk
    global zoom
    global label
    global root
    print( threading.currentThread().getName(), 'Starting')
    
    ###### tinker stuff#############################################
    root = tkinter.Tk()
    label = tkinter.Label( root )
    ######label.bind("<KeyPress>", keydown)
    label.pack()
    frame = tkinter.Frame(root, width=10, height=10)
    frame.bind("<Key>", keydown)
    frame.bind("<Button-1>", callback)
    frame.pack()
    frame.focus_set()
    img = None
    tkimg = [None]  # This, or something like it, is necessary because if you do not keep a reference to PhotoImage instances, they get garbage collected.
    #mam= CircleMarker(  ( 50.0 , 15.0 ), 'blue', 10)
    #mam= CircleMarker(  ( 49.0 , 15.0 ), 'blue', 10)
    #m1.add_marker( mam )
    #image=m1.render(zoom=8, center=(15.,49.))

    #tkimg[0] = ImageTk.PhotoImage(image)
    #label.config(image=tkimg[0])
    ###tkimg = ImageTk.PhotoImage(image)

    delay = 500   # in milliseconds
    #img = Image.new('1', (100, 100), 0)
    print('worTKI: ... ... i wait with TKINTER ON')
    loop()
    root.mainloop()
    print('worTKI: ... ... i should never  die')
    print('worTKI: ... ... i decide to die')
    print('worTKI: ... ... i decide to die')
    return




def worker(context=None):
    '''
    The first worker I did= it just displays the text line on the screen
    '''
    print( threading.currentThread().getName(), 'Starting')
    
    context = context or zmq.Context.instance()
    # receive from master
    receiver = context.socket(zmq.PAIR)
    receiver.connect("inproc://worker")
    print('WORKER: ... ... waiting from master')
    string = receiver.recv()
    print('WORKER: ... ... GOT from master ')
    for i in range(3600*24*365):
        string = receiver.recv()
        #print( '    ',string.decode('utf8') )
        print(' '+gps_info['fix']+gps_info['timex']+
              " ({:6.4f},{:6.4f}){:6.1f} km/h {:6.1f} m H{:03.0f}  {:.1f}     \r".format( gps_info['XCoor'],gps_info['YCoor'],gps_info['speed']*1.852,gps_info['altitude'],gps_info['course'],  gps_info['dist']*1000  ) ,end='\r')
#        # not me -- translate_gp_line()

        if gps_info['fix']=='+' and gps_info['dist']>0.:
             mam= CircleMarker( (gps_info['XCoor'],gps_info['YCoor']),'red', 1)
             m1.add_marker(mam)
             image=m1.render(zoom=zoomset[zoom])
# #                        center=(gps_info['XCoor'],gps_info['YCoor'])  )
             image=image.resize( (int(IMX* resizeF) , int(IMY*resizeF) ) )
              #print('save')
             image.save('map.jpg')
    #time.sleep(5)
    print('WORKER: ... ... i decide to die')
    return



# Prepare our context and sockets
context = zmq.Context.instance()
# Bind to inproc: endpoint, then start upstream thread
sender = context.socket(zmq.PAIR)
sender.bind("inproc://worker")

#sendertki = context.socket(zmq.PAIR)
sendertki = context.socket(zmq.PUB)
#sendertki.bind("inproc://workertki")
sendertki.bind("tcp://*:56543")

threads = []
for i in range(1):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
    t = threading.Thread(target=worker_tki)
    threads.append(t)
    t.start()

print('MASTER: ... "sending to worker"')    
sender.send(b"")
print('MASTER: ... "sending to workerTKI"')    
sendertki.send(b"")

print('MASTER: ... "i am checking threads alive"')
while (1==1):
    alives=True
    for ali in threads:
        print('ASTER:...',ali.isAlive() )
        alives=alives + ali.isAlive()
    if not alives:
        print('MASTER:...breaking')
        print('MASTER:...breaking')
        break
    # USB would be master job
    translate_gp_line()
    print( gps_info['fix'] )
    if gps_info['fix']=='+' and gps_info['dist']>0.:
        MSG=str(gps_info['XCoor'])+':'+str(gps_info['YCoor'])
        print('MASTER:... sending to worker')
        sender.send( MSG.encode('utf8') )

    #print('MASTER...sending to tki')
    #sendertki.send( pickle.dumps( [ gps_info['XCoor'], gps_info['YCoor']  ] ) )
    #sendertki.send( b"" )
    #print('MASTER...sent to tki')

    time.sleep(0.1)
    #print('tock')
print('MASTER: ... "i am free finaly"')

quit()
############################################################# END QUIT



for i in range(9999999):  #115 days
    translate_gp_line()
    #print(i,"    ",gps_info['timex']  )
    #image=m1.render(zoom=8,center=(gps_info['XCoor'],gps_info['YCoor']) )
    if gps_info['fix']=='+' and gps_info['dist']>0.:
        mam= CircleMarker( (gps_info['XCoor'],gps_info['YCoor']),'red', 1)
        m1.add_marker(mam)
        image=m1.render(zoom=zoomset[zoom])
                        #center=(gps_info['XCoor'],gps_info['YCoor'])  )
        image=image.resize( (int(IMX* resizeF) , int(IMY*resizeF) ) )
        #print('save')
        image.save('map.png')
##############
#
#
#
##############



