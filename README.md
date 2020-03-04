# Driver Station 2020

 This code is for Team 41's Driver station in the 2019-2020 season.

  **Make sure to read [the dependency file](dependencies.md)** to install all of the libraries on the appropriate device.

  The code for the Due **must** be used on an Arduino Due for the joystick to work, but the Leonardo can be replaced with any other Arduino, just as long as it has enough ports and communicate via serial pins.

  I will add the contents of [dependencies.md](dependencies.md) here to make it easier to find everything.

  1. Both Raspberry Pi's have Raspbian Buster with Desktop installed and need certain Python libraries which can be installed via `apt`.  The [dependencies file](dependencies.md) contains the exact packages, although most of them will already be installed.
  2. The computer deploying code to the Arduino Due needs to have the joystick library on it. Make sure you use [this one](https://github.com/LordNuke/ArduinoLibs), as it was used in the development of the code and other libraries do not work. Download the file, unzip it, and [add the library to the Arduino IDE](http://interactiondesign.se/wiki/arduino:installing_using_third_party_libraries).

To run the Raspberry Pi GUI's on startup, add the line `@sudo /usr/bin/python3 /home/pi/Top_Pi/top.py` to `/etc/xdg/lxsession/LXDE-pi/autostart`. Change the path of the Python script accordingly.

Run `sudo raspi-config` and go to the Interfacing Options heading. Enable SSH and enable the serial port hardware, but do not enable the serial login shell.

Also, make sure to add the following lines to `/boot/config.txt` to force the 800x480 resolution and rotate the screen 180 degrees.
```
hdmi_group=2
hdmi_mode=87
hdmi_cvt=800 480 60 6 0 0 0
hdmi_drive=1
display_rotate=2
```

When deploying the GUI's to the Pi's, remember to change the line `test = True` to `test = False` in the Python scripts.
