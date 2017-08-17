#!/usr/bin/env python3
#from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import os.path
import cgi
import time

import urllib.request #python3 version   of   urllib
import os
os.chdir("/home/ojr/Maps")

PORT_NUMBER = 8900

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        #DEBUG print('GET entered')
        if self.path=="/":
            self.path="/index.html"

        try:
            #Check the file extension required and
            #set the right mime type

            sendFile = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendFile = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendFile = True
            if self.path.endswith(".png"):
                mimetype='image/png'
                sendFile = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendFile = True
            if self.path.endswith(".ico"):
                mimetype='image/ico'
                sendFile = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendFile = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendFile = True
            #self.path='/map.png'
            #DEBUG print('sendFile at get  = ',sendFile, '. Filename=',self.path)
            if (sendFile == True):
                #DEBUG print('sending file  ... ',self.path)
                #self.path='map.png'
                if (os.path.isfile(curdir+self.path)):         ###### 1 test
                    print('D... file exists ...', curdir+self.path)
                    aassaa=1
                else:
                    print('....file doesnot exist ########################################')
                    whatiwo=self.path
                    zomm=int( whatiwo.split('/')[1])
                    print("D... ZOOM ",zomm)

                    if (zomm==15) or(zomm==12):
                        url='http://a.tile.komoot.de/komoot-2'+whatiwo
                    elif (zomm==8) or(zomm==5):
                        #url='http://a.tile.komoot.de/komoot-2'+whatiwo
                        #url='https://maps.wikimedia.org'+whatiwo
                        url='http://tile.openstreetmap.org'+whatiwo #/%d/%d/%d.png
                        #https://maps.wikimedia.org/#4/40.75/-73.96
                    else:
                        self.send_error(404,'File Not Found: %s' % self.path)
                        print("x... not 15 12 8 5 but ",zomm)
                        return
                    # for more that 15-komoot doesnt work
                    # if zomm>15:
                    #   url='http://a.tile.osm.org'+whatiwo
                                        #         #print("ZOOM=",whatiwo.split('/')[1])
                    # else:
                    #   #url='http://a.tile.osm.org'
                    #   url='http://a.tile.komoot.de/komoot-2'+whatiwo
                    makedir=os.path.dirname(self.path)
                    print('url=',url,'creating dir=', curdir+makedir)
                    if not os.path.exists(curdir+makedir):
                        os.makedirs(curdir+makedir)
                    print('saving to PATH:', curdir+self.path)
                    urllib.request.urlretrieve( url , curdir+self.path)
                    time.sleep(0.7)
                if (os.path.isfile(curdir+self.path)):     ######## 2 final test
                    #DEBUG print('file exists ...')
                    f = open(curdir  + self.path,'rb') 
                    print('serving filename = ' + str( f.name ) +'  close:'+ str( f.closed)  )
                    #print('a')
                    self.send_response(200)
                    self.send_header('Content-type',mimetype)
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                else:
                    print('....file doesnot exist...')
                    self.send_error(404,'File Not Found: %s' % self.path)
            else:
                print('sending internal code:')
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(
                    bytes('<html><body>'+
                        'HELLO. THIS SCRIPT SHOWS inline http code and is example for a server with GET(normal html) and POST(form sending) PARTS<hr>\
                    <form action="send" method="post">\
                    First name:<br>\
                    <input type="text" name="your_name" value="Mickey"><br>\
                    Last name:<br>\
                    <input type="text" name="lastname" value="Mouse"><br><br>\
                    <input type="submit" value="Show me the POST part">\
                    </form>'+
                    '<br>I CAN SEND html jpg png ico gif files from current dir also</body></html>','utf-8'))
            return

        except IOError:
            print('send ioerror')
            self.send_error(404,'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
        print('POST entered : path=',self.path )
        if self.path=="/send":   # this is a section in POST
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })
            print( form.keys() )
            print( "Your name is: %s" % form["your_name"].value)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            aaa=''
            for k in form.keys() :
                aaa=aaa + form[k].value +'\n' ;
                print( k, form[ k].value )
            self.wfile.write( bytes('<html><body>'+
                'WE ARE IN POST PART NOW<br><br>Thanks '+ form["your_name"].value + '. <br>'+
                str(form.keys())+aaa+
                '</body></html>','utf-8') )
            return          
try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print( 'Started httpserver on port ' , PORT_NUMBER)
    
    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print( '^C received, shutting down the web server')
    server.socket.close()
