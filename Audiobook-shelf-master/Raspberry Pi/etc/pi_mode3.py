import RPi.GPIO as GPIO
import time
import json
import threading
import pi_button as b
import pi_bsmith3 as epaper
import pi_stepper as motor
import pi_down_boto3 as boto3
import pi_data as data
import pi_participants_info as ptc

p=ptc.participant('p3')

#booknums
shelfNum =0
onNum=1

#flags
paperFlag =0
motorFlag =0
nowFlag=0
allFlag=0

#counts
allCount=0
countShelf=1

#dictionary
basic_data={}
cur_data={}
prg_data={}


#lists
ad_lists=[]
cur_lists=[]
prg_lists=[]

#most recently listend
rct_listen=''
cur_progress=0


'''
def thread_s3():
    try:
        print('get %s data'%p.name)
        boto3.getData(p.name)
        s3timer=threading.Timer(60, thread_s3)
        s3timer.start()

    except:
        s3timer.cancel()
        print('boto3 get error')
'''
def thread_data():
    try:
        global basic_data
        global cur_data
        global prg_data
        global ad_lists
        global cur_lists
        global prg_lists
       

        print('get %s data from s3'%p.name)
        boto3.getData(p.name)

        #print('read %s data'%p.name)
        basic_data=data.readBasic(p.name)
        cur_data=data.readCur(p.name)
        prg_data=data.readPrg(p.name)

        ad_lists=list(basic_data)
        cur_lists = list(cur_data)
        prg_lists = list(prg_data)

        #print('%s ad_lists is : '%p.name, ad_lists)
        #print('%s cur_lists is : '%p.name, cur_lists)
        print('%s most recently listened is : '%p.name, cur_data['most_recent_adb'])
        #print('%s prg_lists is : '%p.name, prg_lists)

        dtimer=threading.Timer(60, thread_data)
        dtimer.start()

    except:
        dtimer.cancel()
        print('reading data error')


def thread_shelf():
    try:
        global shelfNum
        global countShelf
        global paperFlag
        global motorFlag

        if (countShelf%5) == 0:
            print('nextImage')
            shelfNum+=1
            paperFlag=0
            if shelfNum > (len(ad_lists)-1):
                shelfNum = 0
                countShelf = 1
        if b.read('sh') == True:
            print('stop')
            countShelf=1
            paperFlag=0
            shelfNum=0
            motorFlag=0
            return

        stimer=threading.Timer(1, thread_shelf)
        stimer.start()
        print(countShelf, paperFlag, shelfNum, motorFlag)
        countShelf+=1
    except:
        stimer.cancel()
        print('shelf thread error')


def thread_OnAll():
    try:
        global nowFlag
        global allCount
        global allFlag
        global onNum

        print(allCount)
        allCount+=1

        if (allCount)%60 == 0:
            print('stop')
            allCount=0
            nowFlag=0
            allFlag=0
            onNum=0
            return

        if b.read('sh')==False:
            print('stop')
            allCount=0
            nowFlag=0
            allFlag=0
            return

        timer=threading.Timer(1, thread_OnAll)
        timer.start()

    except:
        timer.cancel()
        print('ongoing_all thread error')




motor.ResetMotor()
thread_data()
cur_progress=0


try:

        while True:

            if b.read('sh') == True:

                if rct_listen != cur_data['most_recent_adb']:
                    epaper.changePIL(p.name, cur_data['most_recent_adb'])
 
                if cur_progress!=prg_data[cur_data['most_recent_adb']]['overall_prg']:  
                    cur_progress=motor.move(cur_progress, prg_data[cur_data['most_recent_adb']]['overall_prg'])
    
                if nowFlag==0 :
                    print('Ongoing_Now')
                    epaper.changePIL(p.name, cur_data['most_recent_adb'])
                    cur_progress=motor.move(cur_progress, prg_data[cur_data['most_recent_adb']]['overall_prg'])
                    rct_listen = cur_data['most_recent_adb']
                    nowFlag=1
                else:
                    if b.read('sb') == True:
                        print('Ongoing_All', onNum)
                        time.sleep(0.5)
                        epaper.changePIL(p.name, cur_lists[onNum])
                        
                        if allFlag == 0:
                            allCount=0
                            cur_progress=motor.move(cur_progress, prg_data[cur_lists[onNum]]['overall_prg'])
                            thread_OnAll()
                            allFlag=1
                        else:
                            allCount=0
                            cur_progress=motor.move(cur_progress, prg_data[cur_lists[onNum]]['overall_prg'])
                            allCount=0

                        if onNum==(len(cur_lists)-2):
                            onNum=0
                        else:
                            onNum=onNum+1

            else:
                print('ShelfMode')
                #print('paperFlag = ', paperFlag)
                #print('motorFlag = ', motorFlag)
                while b.read('sh') == False:
                    if paperFlag==0:
                        epaper.changePIL(p.name, ad_lists[shelfNum])
                        if motorFlag ==0:
                            motor.ResetMotor()
                            time.sleep(0.5)
                            thread_shelf()
                            cur_progress=0
                            motorFlag =1
                        paperFlag=1


except KeyboardInterrupt:
        GPIO.cleanup()


