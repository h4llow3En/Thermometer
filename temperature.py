__author__ = 'h4llow3En'

import dhtreader

def dht_init():
    dhtreader.init()

def get_data(dht, pin):
    data = str(dhtreader.read(dht, pin))
    print data
    return eval(data)
