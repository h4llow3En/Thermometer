#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'h4llow3En'

import time
import datetime
import display
import temperature
import imp

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
    display.start()
    display.display_init()
    #  display.create_char(0x40, degree_pat)
    #  display.create_char(0x41, arrow_up_pat)
    #  display.create_char(0x42, arrow_down_pat)
    temperature.dht_init()
    display.welcome_screen()
    time.sleep(5)
    run()


def run():
    old_temp = 0
    old_hum = 0
    while True:
        timestamp = str(datetime.datetime.now().strftime("%H:%M"))
        try:
            temp, hum = temperature.get_data(dht, pin)
            old_temp, old_hum = temp, hum
        except TypeError:
            temp, hum = old_temp, old_hum
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
