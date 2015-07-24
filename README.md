Thermometer
===========

This project uses an Adafruit DHT22 and a 4 row HD44780 LCD-Display to turn your Raspberry Pi into a thermometer that tracks the temperature and humidity.

Table of contents
-----------------
- [Preferences](#preferences)
- [RPi and display](#rpi-and-display)
- [DHT22 soldering](#dht22-soldering)
- [Features](#features)

Preferences
-----------

* Raspberry Pi Model B
* Adafruit DHT22
* HD44780 4x20 LCD-Display
* Python 2.7 at your Raspberry Pi

RPi and display
---------------

The following Pins on your RPi are used:

![piPin](/documentation/piPin.png)


| Pin| Usage                 | Pin| Usage |
| -- | --------------------- | -- | ----- |
|  1 | Power DHT22 and LED + | 16 | DATA6 |
|  2 | Power HD44780         | 18 | DATA5 |
|  6 | Common Ground (GND)   | 22 | DATA4 |
|  7 | Data from DHT22       | 24 | E     |
| 12 | DATA7                 | 26 | RS    |

It is recommended to use a breadboard.

The HD44780:

![hd44780Pin](/documentation/hd44780Pin.png)

Connect the pins as shown in the graphic. You can use an additional 10K resistor at 'Contrast'. The LED + could be connected to 5V but in my case it was to bright.

DHT22 soldering
---------------
If you have an Adafruit DHT22 without preinstalled resistor, use the following soldering instructions else ignore the soldering and just connect it (Pin 3 is GND then):

![DHT22](/documentation/dht22.png)

You have four pins at the DHT22.

| Pin DHT22 | Description |
| --------- | ----------- |
| 1         | 3.3 Volt    |
| 2         | Data        |
| 3         | not needed  |
| 4         | GND         |

You have to solder (or wire on your breadboard) an additional 10k resistor from positive voltage to the wire coming from the data pin.




Features
--------

* Auto setup (if needed)
* Collect sensordata
* Print data on display (time, temperature, humidity)
* Reusable class for display
* Hardwareinstructions
