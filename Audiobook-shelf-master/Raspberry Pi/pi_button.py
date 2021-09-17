import RPi.GPIO as GPIO
import time

debug=True

GPIO.setmode(GPIO.BCM)
pin_mh = 16
pin_sb = 12 #23
pin_sh = 21 # 18
pin_lh = 20


GPIO.setup(pin_sb, GPIO.IN) # selector button
GPIO.setup(pin_sh, GPIO.IN) # selector hall
GPIO.setup(pin_mh, GPIO.IN)
GPIO.setup(pin_lh, GPIO.IN)

def readAll():
    input_sh = GPIO.input(pin_sh)
    input_sb = GPIO.input(pin_sb)
    input_mh = GPIO.input(pin_mh)
    input_lh = GPIO.input(pin_lh)
    if debug == True:
        print(input_sh, input_sb, input_mh, input_lh)

def read(button):
    input_sh = GPIO.input(pin_sh)
    input_sb = GPIO.input(pin_sb)
    input_mh = GPIO.input(pin_mh)
    input_lh = GPIO.input(pin_lh)

    if button == 'sh':
        return input_sh
    elif button == 'sb':
        return input_sb
    elif button == 'mh':
        return input_mh
    elif button == 'lh':
        return input_lh
    else:
        print('wrong button')


def read_sh(self):
    input_sh = GPIO.input(pin_sh)
    if debug == True:
        print(input_sh)
    return input_sh

def read_sb(self):
    input_sb = GPIO.input(pin_sb)
    if debug == True:
        print(input_sb)
    return input_sb

def read_mh(self):
    input_mh = GPIO.input(pin_mh)
    if debug == True:
        print(input_mh)
    return input_mh

#while True:
#    readAll()
