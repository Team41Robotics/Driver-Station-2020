import button
from tkinter import Tk
from tkinter import PhotoImage
from tkinter import Canvas
from tkinter import CENTER
from tkinter import RIGHT
from tkinter import LEFT
import math

test = True

if (test):
    import fakeSerial as serial
else:
    import serial



ser = serial.Serial("/dev/ttyAMA0", 9600) # /dev/ttyAMA0 on the pi

root = Tk()

# Variables
height = 480
width = 800
btnW = 225
btnH = 250
numButtons = 3

# Delay between pushes (ms)
delay = 10

# Button Dimensions and button objects
btnX = (width-(numButtons*btnW))/(numButtons+1)
btnY = height-btnH-btnX
b1 = button.Button('btn1', btnX, btnY, btnW, btnH, "Position 1")
b2 = button.Button('btn2', (2*btnX) + btnW, btnY, btnW, btnH, "Position 2")
b3 = button.Button('btn3', (3*btnX) + (2*btnW), btnY, btnW, btnH, "Position 3")

# Exit button - top left
ex = button.Button('exit', 0, 0, 25, 25, "X", "red")

ctx = Canvas(root, width=width, height=height, background="black")
ctx.pack()

def handle_click(event):
    event.x = math.fabs(event.x-800)
    event.y = math.fabs(event.y-480)
    # If any of the buttons are clicked, theere is a new line saying "selected"
    # and set the others to the position name, otherwise set them all to the position
    b1.checkClicked(event) 
    b2.checkClicked(event)
    b3.checkClicked(event)
    ex.checkClicked(event)
    if (b1.isClicked):
        print("clicked")
        b1.text_active = "Position 1\nSelected"
        b2.text_active = "Position 2"
        b3.text_active = "Position 3"
    elif (b2.isClicked):
        print("clicked")
        b1.text_active = "Position 1"
        b2.text_active = "Position 2\nSelected"
        b3.text_active = "Position 3"
    elif (b3.isClicked):
        print("clicked")
        b1.text_active = "Position 1"
        b2.text_active = "Position 2"
        b3.text_active = "Position 3\nSelected"
    elif (ex.isClicked):
        exit()
    else:
        b1.text_active = "Position 1"
        b2.text_active = "Position 2"
        b3.text_active = "Position 3"
    drawStuff()




def drawStuff():
    # Draw different Starting Positions
    b1.drawButton(ctx)
    b2.drawButton(ctx)
    b3.drawButton(ctx)
    ex.drawButton(ctx)
    # Text at top
    ctx.create_text(400, 50, justify=CENTER, text="Choose a starting position", font = ("Comic Sans MS", 32), fill="White")
    # Draw the field
    ctx.create_rectangle(0, height/2.75, width, (height/2.75)+10, fill="white", tag="starting line")
    # Exit button
    exit

drawStuff()

ctx.bind("<Button-1>", handle_click)
ctx.pack()  



def publish():
    if (b1.isClicked):
        ser.write(b'\x01')
    elif (b2.isClicked):
        ser.write(b'\x02')
    elif (b3.isClicked):
        ser.write(b'\x03')
    root.after(delay, publish)

root.after(delay, publish)
root.mainloop()