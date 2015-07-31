#!/usr/bin/env python

import RPi.GPIO as GPIO
import os
import glob
import time
import requests
import twil
import datetime
GPIO.setmode(GPIO.BCM)
DEBUG = 1

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

while True:
        channel = 0
        x={}
        lat=41.1458831
        lon=-81.3333331
        value = readadc(channel, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print "value:", value
	x=read_temp()
        print "Temperature Cel:",x[0]
        print "Temperature Frn:",x[1]	
	req = requests.get("http://data.sparkfun.com/input/aGOE6rY5mxcxX1GNnOKq?" +
		"private_key=KEo9nBl42xsZjRg94751" +
		"&user=vtangutu"
		"&latitude=" 	+ str(lat) +
		"&longitude=" 	+ str(lon) +
		"&temperature=" + str(x[0]) +
		"&light=" 	+ str(value) +
		"&zip=44240"
	)
        now = datetime.datetime.now()
        if now.hour == 20 and now.minute > 00 and now.minute < 10:
           twil.mes(x[0])
        print req.status_code
        print now.hour
        time.sleep(360)
