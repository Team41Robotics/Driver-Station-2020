from button import Button
from tkinter import Tk, PhotoImage, Canvas, CENTER, RIGHT, LEFT
import math
from PIL import Image, ImageTk

test = True

if test:
    import fakeSerial as serial
else:
    import serial


ser = serial.Serial("/dev/ttyAMA0", 9600)  # /dev/ttyAMA0 on the pi

root = Tk()

# Variables
height = 480
width = 800
color_inactive = "white"
color_active = "green"

# Delay between pushes (ms)
delay = 10

# Limelight zoom buttons
btnW = 100
btnH = 100
btnX = 425
btnY = 115
padding = 25
b1 = Button('1x', btnX, btnY, btnW, btnH, '1x', color_active)
b2 = Button('2x', btnX + btnW + padding, btnY, btnW, btnH, '2x', color_inactive)
b3 = Button('3x', btnX + (btnW + padding)*2, btnY, btnW, btnH, '3x', color_inactive)

# Intake mode buttons
btnW = 170
btnH = 120
btnX = 420
btnY = 340
padding = 20
b4 = Button('manual', btnX, btnY, btnW, btnH, 'Manual', color_active)
b5 = Button('auto', btnX + btnW + padding, btnY, btnW, btnH, 'Auto', color_inactive)

# Hook buttons
hook0 = ImageTk.PhotoImage(Image.open('./hook0.png'))
hook1 = ImageTk.PhotoImage(Image.open('./hook1.png'))
hook2 = ImageTk.PhotoImage(Image.open('./hook2.png'))
b6 = Button('go', 100, 300, 200, 100, 'Go', color_inactive)

# Exit button - top left
ex = Button('exit', 0, 0, 25, 25, "X", "red")

# All buttons
btns = [b1, b2, b3, b4, b5, b6, ex]

# Canvas object
ctx = Canvas(root, width=width, height=height, background="black")
ctx.pack()

ctx.create_line(width/2, 0, width/2, height, fill="white")
ctx.create_line(width/2, height/2, width, height/2, fill="white")

# Text at top
ctx.create_text(600, 60, justify=CENTER, text="Limelight zoom", font=("Arial", 28), fill="White")
ctx.create_text(600, 300, justify=CENTER, text="Intake mode", font=("Arial", 28), fill="White")

def handle_click(event):
    if not test:
        event.x = math.fabs(event.x-800)
        event.y = math.fabs(event.y-480)

    # If any of the buttons are clicked, theere is a new line saying "selected"
    # and set the others to the position name, otherwise set them all to the position
    for btn in btns: btn.checkClicked(event)

    if ex.isClicked: exit()

    if b1.isClicked:
        b1.color = color_active
        b2.color = color_inactive
        b3.color = color_inactive
    elif b2.isClicked:
        b1.color = color_inactive
        b2.color = color_active
        b3.color = color_inactive
    elif b3.isClicked:
        b1.color = color_inactive
        b2.color = color_inactive
        b3.color = color_active

    if b4.isClicked:
        b4.color = color_active
        b5.color = color_inactive
    elif b5.isClicked:
        b4.color = color_inactive
        b5.color = color_active
    
    drawStuff()


def drawStuff():
    # Draw different Starting Positions
    for btn in btns: btn.drawButton(ctx)


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
