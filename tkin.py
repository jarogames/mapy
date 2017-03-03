#!/usr/bin/env python3
### PIL for printing on png file
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

################ TK to display
import tkinter
from PIL import Image, ImageTk
     
def keydown(e):
    if len(e.char)==0: return
    if e.char==' ':
        print('space')
    else:
        print('   /'+e.char+'/=', ord(e.char) )
def callback(event):
    frame.focus_set()
    print( "clicked at", event.x, event.y)
###### tinker stuff#############################################
root = tkinter.Tk()
label = tkinter.Label(root)
######label.bind("<KeyPress>", keydown)
label.pack()
frame = tkinter.Frame(root, width=100, height=100)
frame.bind("<Key>", keydown)
frame.bind("<Button-1>", callback)
frame.pack()
frame.focus_set()

img = None
tkimg = [None]  # This, or something like it, is necessary because if you do not keep a reference to PhotoImage instances, they get garbage collected.
delay = 500   # in milliseconds
#img = Image.new('1', (100, 100), 0)




def loop():


    #tkimg[0] = ImageTk.PhotoImage(image)
    #label.config(image=tkimg[0])
                ###################################################
    root.update_idletasks()
    root.after( delay, loop )



#neve happens
loop()
#task.wait()
root.mainloop()

