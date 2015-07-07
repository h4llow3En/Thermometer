__author__ = 'h4llow3En'

import subprocess
import os

def setup():
    print "Install python-dev"
    subprocess.call('sudo apt-get install python-dev', shell=True)

    print("Install bcm2835 library")
    subprocess.call('wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.42.tar.gz', shell=True)
    subprocess.call('tar zxvf bcm2835-1.42.tar.gz', shell=True)
    os.chdir(os.getcwd() + '/bcm2835-1.42')
    subprocess.call('./configure', shell=True)
    subprocess.call('make', shell=True)
    subprocess.call('sudo make check', shell=True)
    subprocess.call('sudo make install', shell=True)
    os.chdir(os.getcwd() + '/..')

    print "Building dhtreader"
    subprocess.call('git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git', shell=True)
    os.chdir(os.getcwd() + '/Adafruit-Raspberry-Pi-Python-Code/Adafruit_DHT_Driver_Python')
    subprocess.call('sudo python setup.py build', shell=True)
    subprocess.call('sudo python setup.py install', shell=True)
    os.chdir(os.getcwd() + '/../..')

    print "Cleaning up"
    subprocess.call('sudo rm -r bcm2835-1*', shell=True)
    subprocess.call('sudo rm -r Adafruit-Raspberry-Pi-Python-Code', shell=True)