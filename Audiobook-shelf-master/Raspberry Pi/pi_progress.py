import json
import RPi.GPIO as GPIO, time
import pi_stepper as motor
import pi_participants_info as ptc

GPIO.setmode(GPIO.BCM)
p=ptc.participant('p1')
cur_progress = 0

def move(cur_progress, changed_progress):
    try:
        amount = (changed_progress-cur_progress)

        if amount < 0 :
                direction = False

        else:
                direction = True

        step = round(abs(amount)*59.5)
        #return(dir, step)
        motor.SpinMotor(direction, step)

        cur_progress = changed_progress
        print(amount, direction, step)
        return cur_progress
    except:
        print('somthing wrong')

'''
motor.ResetMotor()
with open(p.prg_filename, 'r') as f:
    prg_data=json.load(f)
    print(json.dumps(prg_data, ensure_ascii=False, indent="\t"))
    
prg_lists = list(prg_data)

for i in range(0, len(prg_lists)):
    print(prg_data[prg_lists[i]]['overall_prg'])

time.sleep(5)

for i in range(0, len(prg_lists)):
    print(prg_data[prg_lists[i]]['overall_prg'])

    cur_progress=move(cur_progress, prg_data[prg_lists[i]]['overall_prg'])
    time.sleep(2)
    print(cur_progress)
'''


