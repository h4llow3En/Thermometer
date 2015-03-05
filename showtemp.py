#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import os
import thread
import welcome
import RPi.GPIO as GPIO

# Zuordnung der GPIO Pins (ggf. anpassen)
DISPLAY_RS = 7
DISPLAY_E = 8
DISPLAY_DATA4 = 25
DISPLAY_DATA5 = 24
DISPLAY_DATA6 = 23
DISPLAY_DATA7 = 18

DISPLAY_WIDTH = 20  # Zeichen je Zeile
DISPLAY_LINE_1 = 0x80  # Adresse der ersten Display Zeile
DISPLAY_LINE_2 = 0xC0  # Adresse der zweiten Display Zeile
DISPLAY_LINE_3 = 0x94  # Adresse der dritten Display Zeile
DISPLAY_LINE_4 = 0xD4  # Adresse der vierten Display Zeile
DISPLAY_CHR = True
DISPLAY_CMD = False
E_PULSE = 0.00005
E_DELAY = 0.00005


def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DISPLAY_E, GPIO.OUT)
    GPIO.setup(DISPLAY_RS, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA4, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA5, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA6, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA7, GPIO.OUT)
    display_init()
    dir = os.path.abspath(os.curdir)
    welcome.welcome_screen()
    thread.start_new_thread(sensor(dir))
    thread.start_new_thread(marquee(dir))


def sensor(dir):
    tmp_old = 0
    hum_old = 0
    path_s = dir + "/Sensor.sh"
    path_l = dir + "/Temp/log.dat"

    while True:

        timestamp = str(datetime.datetime.now().strftime("%H:%M"))
        os.system(path_s)
        log = open(path_l).readlines()
        if (log[0] != '') and (log[0] != '\n') and (log[1] != '') and (log[1] != '\n'):
            tmp = float(log[0])
            tmp_old = tmp
            hum = float(log[1])
            hum_old = hum
        else:
            tmp = tmp_old
            hum = hum_old

        display_out(1, "Time: " + str(timestamp))
        display_out(2, "Temp: " + str(tmp) + " " + u'\xb0' + "C")
        display_out(3, "Humidity: " + str(hum) + "%")

    time.sleep(10)


def marquee(dir):
    text_path = dir + '/text.txt'
    text = open(text_path).read() + " "
    length = len(text)
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    while True:
        text_show = ''
        x = 0
        for x in range(0, 20, ):
            a[x] = a[x] % length
            text_show = text_show + text[a[x]]
            a[x] = a[x] + 1
        display_out(4, str(text_show))

        time.sleep(0.5)


def display_out(line, string):
    if (line == 1):
        ln = DISPLAY_LINE_1
    elif (line == 2):
        ln = DISPLAY_LINE_2
    elif (line == 3):
        ln = DISPLAY_LINE_3
    elif (line == 4):
        ln = DISPLAY_LINE_4

    lcd_byte(ln, DISPLAY_CMD)
    lcd_string(string)


def display_init():
    lcd_byte(0x33, DISPLAY_CMD)
    lcd_byte(0x32, DISPLAY_CMD)
    lcd_byte(0x28, DISPLAY_CMD)
    lcd_byte(0x0C, DISPLAY_CMD)
    lcd_byte(0x06, DISPLAY_CMD)
    lcd_byte(0x01, DISPLAY_CMD)


def lcd_string(message):
    message = message.ljust(DISPLAY_WIDTH, " ")
    for i in range(DISPLAY_WIDTH):
        lcd_byte(ord(message[i]), DISPLAY_CHR)


def lcd_byte(bits, mode):
    GPIO.output(DISPLAY_RS, mode)
    GPIO.output(DISPLAY_DATA4, False)
    GPIO.output(DISPLAY_DATA5, False)
    GPIO.output(DISPLAY_DATA6, False)
    GPIO.output(DISPLAY_DATA7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(DISPLAY_DATA4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(DISPLAY_DATA5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(DISPLAY_DATA6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(DISPLAY_DATA7, True)
    time.sleep(E_DELAY)
    GPIO.output(DISPLAY_E, True)
    time.sleep(E_PULSE)
    GPIO.output(DISPLAY_E, False)
    time.sleep(E_DELAY)
    GPIO.output(DISPLAY_DATA4, False)
    GPIO.output(DISPLAY_DATA5, False)
    GPIO.output(DISPLAY_DATA6, False)
    GPIO.output(DISPLAY_DATA7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(DISPLAY_DATA4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(DISPLAY_DATA5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(DISPLAY_DATA6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(DISPLAY_DATA7, True)
    time.sleep(E_DELAY)
    GPIO.output(DISPLAY_E, True)
    time.sleep(E_PULSE)
    GPIO.output(DISPLAY_E, False)
    time.sleep(E_DELAY)


if __name__ == '__main__':
    main()
