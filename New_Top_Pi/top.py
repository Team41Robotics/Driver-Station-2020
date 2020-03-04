from button import Button
from tkinter import Tk, PhotoImage, Canvas, CENTER, RIGHT, LEFT, N
import math
from PIL import Image, ImageTk

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
color_active = "green"

# Delay between pushes (ms)
delay = 10

# Limelight zoom buttons
btnW = 100
btnH = 100
btnX = 425
btnY = 115
padding = 25
b1 = Button('1x', btnX, btnY, btnW, btnH, '1x', color_active, 32)
b2 = Button('2x', btnX + btnW + padding, btnY, btnW, btnH, '2x', color_inactive, 32)
b3 = Button('3x', btnX + (btnW + padding)*2, btnY, btnW, btnH, '3x', color_inactive, 32)

# Intake mode buttons
btnW = 170
btnH = 120
btnX = 420
btnY = 340
padding = 20
b4 = Button('manual', btnX, btnY, btnW, btnH, 'Manual', color_active, 32)
b5 = Button('auto', btnX + btnW + padding, btnY, btnW, btnH, 'Auto', color_inactive, 32)

# Hook buttons
hook_imgs = ['./hook0.gif','./hook1.gif','./hook2.gif']
hook_msgs = ['Go to pos 1', 'Go to pos 2', 'In manual']
hook_colors = ['white', 'yellow', 'orange']
hook_imgs = [Image.open(x) for x in hook_imgs]
hook_imgs = [ImageTk.PhotoImage(x) for x in hook_imgs]
b6 = Button('go', 100, 350, 200, 100, hook_msgs[0], hook_colors[0], 24)

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
        b3.color = color_inactive
        zoom = 1
    elif b2.isClicked:
        b1.color = color_inactive
        b2.color = color_active
        b3.color = color_inactive
        zoom = 2
    elif b3.isClicked:
        b1.color = color_inactive
        b2.color = color_inactive
        b3.color = color_active
        zoom = 3

    if b4.isClicked:
        b4.color = color_active
        b5.color = color_inactive
        mode = 0
    elif b5.isClicked:
        b4.color = color_inactive
        b5.color = color_active
        mode = 1

    if b6.isClicked:
        hook += 1
        if hook > 2: hook = 0
        b6.text_active = hook_msgs[hook]
        b6.color = hook_colors[hook]
    
    drawStuff()


def drawStuff():
    for btn in btns: btn.drawButton(ctx)

    ctx.delete('hook_img')
    ctx.create_image(200, 10, anchor=N, image=hook_imgs[hook], tag='hook_img')


drawStuff()

ctx.bind("<Button-1>", handle_click)
ctx.pack()


def publish():
    val = 0
    if hook == 1:
        val = 3
    elif hook == 2:
        val = 7
    else:
        val = (mode << 2) | (zoom - 1)
    ser.write(val.to_bytes(1, byteorder='big'))
    root.after(delay, publish)


root.after(delay, publish)
root.mainloop()
