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

ser = serial.Serial("/dev/tty", 9600)  # /dev/ttyAMA0 on the pi

root = Tk()

# Variables
img = PhotoImage(file="./Zoom.gif", format="gif")
img2 = img.subsample(2)
img3 = img2.subsample(2)
imageTable = [img3, img2, img]
height = 480
width = 800
btnW = 250
btnH = 125
numButtons = 3

# Delay between pushes (ms)
delay = 10

# Button Dimensions and button objects
btnX = 2 * (width / 3)
btnY = (height - (numButtons * btnH)) / (numButtons + 1)
b1 = button.Button('btn1', btnX, btnY, btnW, btnH, "1x Zoom")
b2 = button.Button('btn2', btnX, (2 * btnY) + btnH, btnW, btnH, "2x Zoom")
b3 = button.Button('btn3', btnX, (3 * btnY) + (2 * btnH), btnW, btnH, "3x Zoom")

# Exit button - top left
ex = button.Button('exit', 0, 0, 25, 25, "X", "red")

ctx = Canvas(root, width=width, height=height, background="#4f3714")
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
    if b1.isClicked:
        b1.color_active = "red"
        b2.color_active = b2.color
        b3.color_active = b3.color
        zoomLevel = 1
    elif b2.isClicked:
        b1.color_active = b1.color
        b2.color_active = "red"
        b3.color_active = b3.color
        zoomLevel = 2
    elif b3.isClicked:
        b1.color_active = b1.color
        b2.color_active = b2.color
        b3.color_active = "red"
        zoomLevel = 3
    elif ex.isClicked:
        exit()
    drawStuff(zoomLevel)


def drawStuff(zoomLevel):
    # Draw different Starting Positions
    imgwidth= width/3
    imgheight= height/1.8
    b1.drawButton(ctx)
    b2.drawButton(ctx)
    b3.drawButton(ctx)
    ex.drawButton(ctx)
    # Text at top
    ctx.delete("image")
    ctx.create_text(width / 3, 50, justify=CENTER, text="Choose Limelight Zoom", font=("Comic Sans MS", 32),
                    fill="White", tag="image")
    # Zoom image
    if zoomLevel in [1,2,3]:
        ctx.delete('zoom')
        ctx.create_image(imgwidth, imgheight , image= imageTable[zoomLevel-1], anchor=CENTER, tag='zoom')

drawStuff(1)

ctx.bind("<Button-1>", handle_click)
ctx.pack()


def publish():
    if b1.isClicked:
        ser.write(b'\x01')
    elif b2.isClicked:
        ser.write(b'\x02')
    elif b3.isClicked:
        ser.write(b'\x03')
    root.after(delay, publish)


root.after(delay, publish)
root.mainloop()
