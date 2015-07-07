__author__ = 'h4llow3En'

from display import *

def welcome_screen():
    lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
    lcd_string("Wetterstation BETA")
    lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
    lcd_string("Copyright 2014 by Felix Doering")

    time.sleep(5)