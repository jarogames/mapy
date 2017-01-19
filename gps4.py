#!/usr/bin/env python3
import subprocess
import pandas as pd

df = pd.DataFrame()
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
    if (lin.find('GPGGA')>0):
        time=lin.split(',')[1]
        print( fix, time[0:2]+':'+time[2:4]+':'+time[4:8],' UTC' )#df=pd.concat(
    if (lin.find('GPGLL')>0):
        print(lin)

#    else:
#        print("NOT",lin)
task.wait()
