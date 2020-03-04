# Driver Station 2020

 This code is for Team 41's Driver station in the 2019-2020 season.

  **Make sure to read [the dependency file](dependencies.txt)** to install all of the libraries on the appropriate device.

  The code for the Due **must** be used on an Arduino Due for the joystick to work, but the Leonardo can be replaced with any other Arduino, just as long as it has enough ports and communicate via serial pins.

  I will add the contents of [dependencies.txt](dependencies.txt) here to make it easier to find everything.

  1. Both Raspberry Pi's must have Pyserial installed. To install, run the command `sudo apt-get install python3-serial` on the terminal on the Pi. More information about Pyserial can be found [here](https://pythonhosted.org/pyserial/).
  2. Both Raspberry Pi's also need to have tkinter to be able to display graphics. Run `sudo apt-get install python3-tk` to install. More information about it [here](https://docs.python.org/3/library/tk.html).
  3. The computer deploying code to the Arduino Due needs to have the joystick library on it. Make sure you use [this one](https://github.com/LordNuke/ArduinoLibs), as it was used in the development of the code and other libraries do not work. Download the file, unzip it, and [add the library to the Arduino IDE](http://interactiondesign.se/wiki/arduino:installing_using_third_party_libraries).

To run the Raspberry Pi GUI's on startup, add the line `@sudo /usr/bin/python3 /home/pi/Top_Pi/top.py` to `/etc/xdg/lxsession/LXDE-pi/autostart`.

Some other dependencies that the Pi may or may not need can be installed with `sudo apt install git vim python3 python3-pip python3-pil python3-pil.imagetk`
