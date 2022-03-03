from button import Button
from tkinter import Tk, Canvas, CENTER, RIGHT, LEFT, N, PhotoImage
import math
import os

dirname = os.path.dirname(__file__)

test = True

if test:
    import fakeSerial as serial
else:
    import serial


ser = serial.Serial("/dev/ttyAMA0", 9600)  # /dev/ttyAMA0 on the pi

root = Tk()
# Full screen
if not test:
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.focus_set()  #Move focus to this widget
    root.bind("<Escape>", lambda e: root.quit())
    root.config(cursor="none")

# Variables
height = 480
width = 800
color_inactive = "white"
color_active = "#32CD32" # lime green

# Delay between pushes (ms)
delay = 10

# Limelight zoom buttons
# Intake mode buttons
btnY = 340
padding = 20

# Hook buttons
btnX = 20
btnW = 2*250 + padding
btnH = 100
btnY = 360

# Exit button - top left
ex = Button('exit', 0, 0, 25, 25, "X", "red")


btnW = 250
btnH = 120
btnX = 420
btnY = 115
padding = 20
b1 = Button('1x', width/3 - width/4, height/3, btnW, btnH, '1x', color_active, 32)
b2 = Button('2x', width*2/3 - btnW +  width/4, height/3, btnW, btnH, '2x', color_inactive, 32)

# All buttons
btns = [b1, b2, ex]

zoom1x = PhotoImage(file="1xzoom.gif")
zoom2x = PhotoImage(file="2xzoom.gif")
# Canvas object
ctx = Canvas(root, width=width, height=height, background="black")
ctx.pack()


# Text at top
ctx.create_text(width/2, height/5, justify=CENTER, text="Limelight zoom", font=("Arial", 28), fill="White")

ctx.create_image(width/3-width/4+b1.wdith/2, height*4/5, image=zoom1x, tag="1xzoom", anchor=CENTER)
# ctx.create_rectangle(width/3-width/4, height*4/5-90, width/3-width/4+b1.wdith, height*4/5+b1.height/2, outline="green", tag="1xzoomrect")
ctx.create_image(width*2/3 - btnW/2 +  width/4, height*4/5, image=zoom2x, tag="2xzoom", anchor=CENTER)
# ctx.create_rectangle(width/3-width/4, height*4/5-90, width/3-width/4+b1.wdith, height*4/5+b1.height/2, outline="green", tag="1xzoomrect")

# State variables
zoom = 1
mode = 0
hook = 0

def handle_click(event):
    global zoom, mode
    if not test:
        event.x = math.fabs(event.x-800)
        event.y = math.fabs(event.y-480)

    for btn in btns: btn.checkClicked(event)

    if ex.isClicked: exit()

    if b1.isClicked:
        b1.color = color_active
        b2.color = color_inactive
        zoom = 1
    elif b2.isClicked:
        b1.color = color_inactive
        b2.color = color_active
        zoom = 2
    
    drawStuff()


def drawStuff():
    for btn in btns: btn.drawButton(ctx)
    
    ctx.delete('curr_msg')
    ctx.delete('next_msg')
    ctx.delete('next_title')


drawStuff()

ctx.bind("<Button-1>", handle_click)
ctx.pack()


def publish():
    hook_bit = hook & 1
    val = (hook_bit << 2) | (mode << 1) | (zoom - 1) # Lower bit is zoom, second bit is mode, third bit is hook toggle
    if test:
        print('{0:04b}'.format(val))
    ser.write(val.to_bytes(1, byteorder='big'))
    root.after(delay, publish)


root.after(delay, publish)
root.mainloop()
