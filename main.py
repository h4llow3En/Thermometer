#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'h4llow3En'

import time
import datetime
import os
import thread
import display
import RPi.GPIO as GPIO
import temperature
import subprocess
import imp


# Zuordnung der GPIO Pins (ggf. anpassen)
DISPLAY_RS = 7
DISPLAY_E = 8
DISPLAY_DATA4 = 25
DISPLAY_DATA5 = 24
DISPLAY_DATA6 = 23
DISPLAY_DATA7 = 18

DISPLAY_WIDTH = 20
DISPLAY_LINE_1 = 0x80
DISPLAY_LINE_2 = 0xC0
DISPLAY_LINE_3 = 0x94
DISPLAY_LINE_4 = 0xD4
DISPLAY_CHR = True
DISPLAY_CMD = False
E_PULSE = 0.00005
E_DELAY = 0.00005

# custom characters
degree = 0
degree_pat = [8,20,8,6,9,8,9,6]
arrow_up = 1
arrow_up_pat = [0,15,3,5,9,16,0,0]
arrow_down = 2
arrow_down_pat = [0,16,9,5,3,15,0,0]

# sensor config
dht = 22
pin = 4



def main():
    check_setup()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DISPLAY_E, GPIO.OUT)
    GPIO.setup(DISPLAY_RS, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA4, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA5, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA6, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA7, GPIO.OUT)
    display.display_init()
    display.create_char(0x40, degree_pat)
    display.create_char(0x41, arrow_up_pat)
    display.create_char(0x42, arrow_down_pat)


def run():
    while True:
        timestamp = str(datetime.datetime.now().strftime("%H:%M"))
        temp, hum = temperature.get_data(dht, pin)
        display.output(time=timestamp, temp=temp, hum=hum)
        time.sleep(5)


def check_setup():
    try:
        imp.find_module('dhtreader')
        found = True
    except ImportError:
        found = False

    if found is False:
        import setup
        setup.setup()


if __name__ == '__main__':
    main()
