__author__ = 'h4llow3En'


import RPi.GPIO as GPIO
import time

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


def output(time, temp, hum, tempdiff=[]):

    strtime = "Time: {}".format(time)
    strtemp = "Temp: {} ".format(float(int(temp*10))/10)
    strhum = "Humidity: {} %".format(float(int(hum*10))/10)

    #  Time on first line
    lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
    lcd_string(strtime)
    print strtime

    #  Temperature and degree Celsius Sign on second Line
    lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
    lcd_string(strtemp)
    lcd_byte(0, DISPLAY_CMD)
    print strtemp

    #  Humidity on third Line
    lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
    lcd_string(strhum)
    print strhum

    # Show tempdiff if avaidable
    lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
    for value in tempdiff:
        lcd_byte(value, DISPLAY_CMD)


def start():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DISPLAY_E, GPIO.OUT)
    GPIO.setup(DISPLAY_RS, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA4, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA5, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA6, GPIO.OUT)
    GPIO.setup(DISPLAY_DATA7, GPIO.OUT)


def display_init():
    lcd_byte(0x33, DISPLAY_CMD)
    lcd_byte(0x32, DISPLAY_CMD)
    lcd_byte(0x28, DISPLAY_CMD)
    lcd_byte(0x0C, DISPLAY_CMD)
    lcd_byte(0x06, DISPLAY_CMD)
    lcd_byte(0x01, DISPLAY_CMD)


def create_char(CGCHR, char):
    lcd_byte(CGCHR, DISPLAY_CMD)
    if len(char) is 7:
        bytes = char[0], char[1], char[2], char[3], char[4], char[5], char[6]
    else:
        bytes = char[0], char[1], char[2], char[3], char[4], char[5], char[6], char[7]

    for value in bytes:
        lcd_byte(value, DISPLAY_CHR)

    return CGCHR - 0x40


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