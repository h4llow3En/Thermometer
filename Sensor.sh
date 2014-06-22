#!/bin/bash
#Aktuelles Datum mit Uhrzeit einer Variablen zuweisen
while true
do
# Im Skript den Ordner wechseln und die Temperaturdaten auslesen
cd /home/pi/Wetterstation/adafruit/Adafruit-Raspberry-Pi-Python-Code-master/Adafruit_DHT_Driver/

WERTE=$(sudo ./Adafruit_DHT 22 2)
TEMP=( $(echo $WERTE | awk '{print $13}'))
LUFT=( $(echo $WERTE | awk '{print $17}'))

# Ausgabe semikolonsepariert in Datei
echo "$TEMP" > /home/pi/Temperatur/log.dat
echo "$LUFT" >> /home/pi/Temperatur/log.dat
done