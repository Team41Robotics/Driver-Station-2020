from button import Button
from tkinter import Tk, Canvas, CENTER, RIGHT, LEFT, N
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
btnW = 170
btnH = 120
btnX = 420
btnY = 115
padding = 20
b1 = Button('1x', btnX, btnY, btnW, btnH, '1x', color_active, 32)
b2 = Button('2x', btnX + btnW + padding, btnY, btnW, btnH, '2x', color_inactive, 32)

# Intake mode buttons
btnY = 340
padding = 20
b3 = Button('manual', btnX, btnY, btnW, btnH, 'Manual', color_active, 32)
b4 = Button('auto', btnX + btnW + padding, btnY, btnW, btnH, 'Auto', color_inactive, 32)

# Hook buttons
hook_msgs = ['None', 'Start Up', 'Clamp Down', 'Piston Forward', 'Piston Reverse', 'Fork Up', 'Final Up', 'Done']
num_msgs = len(hook_msgs)
btnX = 20
btnW = 2*btnW + padding
btnH = 100
btnY = 360
b5 = Button('next', btnX, btnY, btnW, btnH, 'NEXT', color_inactive, 24)

# Exit button - top left
ex = Button('exit', 0, 0, 25, 25, "X", "red")

# All buttons
btns = [b1, b2, b3, b4, b5, ex]

# Canvas object
ctx = Canvas(root, width=width, height=height, background="black")
ctx.pack()

ctx.create_line(width/2, 0, width/2, height, fill="white")
ctx.create_line(width/2, height/2, width, height/2, fill="white")

# Text at top
ctx.create_text(600, 60, justify=CENTER, text="Limelight zoom", font=("Arial", 28), fill="White")
ctx.create_text(600, 300, justify=CENTER, text="Intake mode", font=("Arial", 28), fill="White")
ctx.create_text(200, 60, justify=CENTER, text="Current state", font=("Arial", 28), fill="White")

# State variables
zoom = 1
mode = 0
hook = 0

def handle_click(event):
    global zoom, mode, hook
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

    if b3.isClicked:
        b3.color = color_active
        b4.color = color_inactive
        mode = 0
    elif b4.isClicked:
        b3.color = color_inactive
        b4.color = color_active
        mode = 1
	
    if b5.isClicked:
        hook += 1
        b5.text_active = "RESET" if hook == num_msgs-1 else "NEXT"
        if hook >= num_msgs: hook = 0
    
    drawStuff()


def drawStuff():
    for btn in btns: btn.drawButton(ctx)
    
    ctx.delete('curr_msg')
    ctx.delete('next_msg')
    ctx.delete('next_title')
    ctx.create_text(200, 120, justify=CENTER, text=hook_msgs[hook], font=("Arial", 36), fill=color_active, tag="curr_msg")
    if hook < num_msgs-1:
        ctx.create_text(200, 240, justify=CENTER, text="Next state", font=("Arial", 28), fill="White", tag="next_title")
        ctx.create_text(200, 300, justify=CENTER, text=hook_msgs[hook+1], font=("Arial", 36), fill=color_active, tag="next_msg")


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
