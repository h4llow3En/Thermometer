#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'h4llow3En'

import time
import datetime
import display
import imp

# custom characters
degree_pat = (
    0b01000,
    0b10100,
    0b01000,
    0b00011,
    0b00100,
    0b00100,
    0b00100,
    0b00011)
arrow_up_pat = (
    0b00000,
    0b01111,
    0b00011,
    0b00101,
    0b01001,
    0b10000,
    0b00000,
    0b00000)
arrow_down_pat = (
    0b00000,
    0b10000,
    0b01001,
    0b00101,
    0b00011,
    0b01111,
    0b00000,
    0b00000)

# sensor config
dht = 22
pin = 4


def main():
    lcd = display.HD44780()
    lcd.create_char(0, degree_pat)
    lcd.create_char(1, arrow_up_pat)
    lcd.create_char(2, arrow_down_pat)
    temperature.dht_init()
    run(lcd)


def run(lcd):
    old_temp = 0
    old_hum = 0
    while True:
        timestamp = str(datetime.datetime.now().strftime("%H:%M"))
        try:
            temp, hum = temperature.get_data(dht, pin)
            temp, hum = float(int(temp*10))/10, float(int(hum*10))/10
            old_temp, old_hum = temp, hum
        except TypeError:
            temp, hum = old_temp, old_hum

        lcd.send_string(timestamp, row=0)
        lcd.send_string("Temp: {} \cg:0".format(temp), row=1)
        lcd.send_string("Humidity: {} %".format(temp))
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

check_setup()
import temperature

if __name__ == '__main__':
    main()
