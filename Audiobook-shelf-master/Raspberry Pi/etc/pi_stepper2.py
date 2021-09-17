#!/usr/bin/python
#import json
import RPi.GPIO as GPIO, time
import pi_button as b
#import pi_stepper as motor
#import pi_participants_info as ptc

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
dirpin = 26
stppin = 19
slppin = 13
speed=3500

GPIO.setup(dirpin, GPIO.OUT) #dir 
GPIO.setup(stppin, GPIO.OUT) #stp
GPIO.setup(slppin, GPIO.OUT) #slp
#GPIO.setwarnings(False)
GPIO.output(stppin, True)

GPIO.output(slppin, False)
#iemand anders 500
p = GPIO.PWM(stppin, 5000)


def SpinMotor(direction, num_steps):

    GPIO.output(slppin, True)
    p.ChangeFrequency(speed)
    GPIO.output(dirpin, direction)
    while num_steps > 0:
        p.start(1)
        time.sleep(0.01)
        num_steps -= 1
        if b.read('mh') == 0:
            if direction == False:
                print('mh detects pendulum')
                p.stop()
                break

        #if b.read('lh') == 0:
        #    if direction == True:
        #        print('lh detects pendulum')
        #        p.stop()
        #        break

        print(b.read('mh'), b.read('lh'))
        print(num_steps)
    p.stop()
    GPIO.output(slppin, False)
    return True

def ResetMotor():
    speed = 5000
    GPIO.output(slppin, True)
    p.ChangeFrequency(speed)
    num_steps = 5800
    '''
    GPIO.output(dirpin, True)
    while b.read('lh') == 1:
        p.start(1)
        time.sleep(0.01)
        num_steps -= 1
        print(num_steps)
        print(b.read('lh'))

    print('lh detects pendulum')
    p.stop()
    time.sleep(2)
    p.ChangeFrequency(speed)
    num_steps = 5800
    '''
    GPIO.output(dirpin, False)
    while b.read('mh') == 1:
        p.start(1)
        time.sleep(0.01)
        num_steps -= 1
        print(num_steps)
        print(b.read('mh'))

    print('mh detects pendulum')
    p.stop()
    GPIO.output(slppin, False)
    return True


'''
def ResetMotor():
    GPIO.output(slppin, True)
    p.ChangeFrequency(speed)
    num_steps = 5950
    GPIO.output(dirpin, False)
    while b.read('mh') == 1:
        p.start(1)
        time.sleep(0.01)
        num_steps -= 1
        print(num_steps)
        print(b.read('mh'))

    print('mh detects pendulum')
    p.stop()
    GPIO.output(slppin, False)
    return True
'''
def move(cur_progress, changed_progress):
   #try:
    amount = (changed_progress-cur_progress)
    if amount < 0 :
            direction = False
    else:
            direction = True

    step = round(abs(amount)*59.5)
    #step = round(abs(amount)*60)
    SpinMotor(direction, step)

    cur_progress = changed_progress
    print(amount, direction, step)
    return cur_progress

    #except:
    #    print('somthing wrong')


#ResetMotor()

'''
direction_input = input('Please enter O or C fro Open or Close:')
num_steps = input('Please enter the number of steps: ')
num_steps = int(num_steps)
if direction_input == 'C':
    SpinMotor(False, num_steps)
elif direction_input == 'R':
    ResetMotor()
else:
    SpinMotor(True, num_steps)

'''
