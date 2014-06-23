#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import os
import RPi.GPIO as GPIO

# Zuordnung der GPIO Pins (ggf. anpassen)
DISPLAY_RS = 7
DISPLAY_E  = 8
DISPLAY_DATA4 = 25 
DISPLAY_DATA5 = 24
DISPLAY_DATA6 = 23
DISPLAY_DATA7 = 18




DISPLAY_WIDTH = 20 	# Zeichen je Zeile
DISPLAY_LINE_1 = 0x80 	# Adresse der ersten Display Zeile
DISPLAY_LINE_2 = 0xC0 	# Adresse der zweiten Display Zeile
DISPLAY_LINE_3 = 0x94   # Adresse der dritten Display Zeile
DISPLAY_LINE_4 = 0xD4   # Adresse der vierten Display Zeile
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
	tmp_old = 0
	hum_old = 0
	pat = os.path.abspath(os.curdir) + "/Sensor.sh"
	print pat

	while True:
		timestmp = str(datetime.datetime.now().strftime("%H:%M"))
		
		log = open("/home/pi/Wetterstation/Temperatur/log.dat").readlines()	
		print log
		if (log[0] != '') and (log[0] != '\n') :
			tmp = float(log[0])
			tmp_old = tmp
			hum = float (log[1])
			hum_old = hum
		else:
			tmp = tmp_old
			hum = hum_old
			
		lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
	      	lcd_string("Time: " + str(timestmp))
		lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
		lcd_string("Temp: " + str(tmp) + " " + u'\xb0' + "C")
		lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
		lcd_string("Humidity: " + str(hum) + "%")
		lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
        	lcd_string("-MAKE THINGS BETTER-")
		os.system(pat)
		time.sleep(5)
		



def display_init():
	lcd_byte(0x33,DISPLAY_CMD)
	lcd_byte(0x32,DISPLAY_CMD)
	lcd_byte(0x28,DISPLAY_CMD)
	lcd_byte(0x0C,DISPLAY_CMD)  
	lcd_byte(0x06,DISPLAY_CMD)
	lcd_byte(0x01,DISPLAY_CMD)  

def lcd_string(message):
	message = message.ljust(DISPLAY_WIDTH," ")  
	for i in range(DISPLAY_WIDTH):
	  lcd_byte(ord(message[i]),DISPLAY_CHR)

def lcd_byte(bits, mode):
	GPIO.output(DISPLAY_RS, mode)
	GPIO.output(DISPLAY_DATA4, False)
	GPIO.output(DISPLAY_DATA5, False)
	GPIO.output(DISPLAY_DATA6, False)
	GPIO.output(DISPLAY_DATA7, False)
	if bits&0x10==0x10:
	  GPIO.output(DISPLAY_DATA4, True)
	if bits&0x20==0x20:
	  GPIO.output(DISPLAY_DATA5, True)
	if bits&0x40==0x40:
	  GPIO.output(DISPLAY_DATA6, True)
	if bits&0x80==0x80:
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
	if bits&0x01==0x01:
	  GPIO.output(DISPLAY_DATA4, True)
	if bits&0x02==0x02:
	  GPIO.output(DISPLAY_DATA5, True)
	if bits&0x04==0x04:
	  GPIO.output(DISPLAY_DATA6, True)
	if bits&0x08==0x08:
	  GPIO.output(DISPLAY_DATA7, True)
	time.sleep(E_DELAY)    
	GPIO.output(DISPLAY_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(DISPLAY_E, False)  
	time.sleep(E_DELAY)   

if __name__ == '__main__':
	main()
