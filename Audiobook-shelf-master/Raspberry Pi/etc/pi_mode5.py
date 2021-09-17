import RPi.GPIO as GPIO
import time
import json
import threading
import pi_button as b
import pi_bsmith3 as epaper
import pi_stepper as motor
import pi_down_boto3 as boto3
import pi_data as data
import pi_interaction as log
import pi_participants_info as ptc

p=ptc.participant('p1')

#booknums
shelfNum =0
onNum=0
index=''

#flags
paperFlag =0
motorFlag =0
nowFlag=0
allFlag=0
finFlag=0

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


def thread_data():
    try:
        global basic_data
        global cur_data
        global prg_data
        global ad_lists
        global cur_lists
        global prg_lists
        global onNum
        global shelfNum
        global index
        global pinFlag

        print('get %s data from s3'%p.name)
        boto3.getData(p.name)

        #print('read %s data'%p.name)
        basic_data=data.readBasic(p.name)
        cur_data=data.readCur(p.name)
        prg_data=data.readPrg(p.name)

        ad_lists=list(basic_data)
        cur_lists = list(cur_data)
        prg_lists = list(prg_data)

        if len(cur_lists) == 1:
            print('empty')
            pinFlag=1
            onNum=0
            shelfNum=0
            index= ''
        else:
            pinFlag=0
            onNum= cur_lists.index(cur_data['most_recent_adb'])+1
            shelfNum= cur_lists.index(cur_data['most_recent_adb'])+1
            index= cur_lists.index(cur_data['most_recent_adb'])


        print('%s most recently listened is : '%p.name, cur_data['most_recent_adb'])
        print('index = ', index, ' onNum = ', onNum)
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
            print('thread shelf stop')
            countShelf=1
            paperFlag=0
            #shelfNum=0

            if finFlag == 1:
                shelfNum=0
            else:
                shelfNum= cur_lists.index(cur_data['most_recent_adb'])+1
            #shelfNum= cur_lists.index(cur_data['most_recent_adb'])+1
            motorFlag=0
            nowFlag=0
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

        print('allCount is : ', allCount)
        #allCount+=1
        
        if (allCount) == 150:
            print('stop_onAll_30')
            return


        if (allCount) == 20:
            print('stop_onAll')
            
            allCount=0
            nowFlag=0
            allFlag=0
            if finFlag ==1:
                onNum=0
            else:
                onNum= cur_lists.index(cur_data['most_recent_adb'])+1
            #onNum=0
            return

        if b.read('sh')==False:
            print('stop_OnAll')
            allCount=0
            nowFlag=0
            allFlag=0
            return

        allCount+=1
        timer=threading.Timer(1, thread_OnAll)
        timer.start()

    except:
        timer.cancel()
        print('ongoing_all thread error')


#motor.Setup()
motor.Reset()
thread_data()
cur_progress=0


try:

        while True:

            if b.read('sh') == True:

                if nowFlag==0 :
                    print('Ongoing_Now')
                    time.sleep(0.5)
                    epaper.changePIL(p.name, cur_data['most_recent_adb'])
                    time.sleep(0.5)
                    log.Log(p.name, 'Ongoing_Now', cur_data['most_recent_adb'], prg_data[cur_data['most_recent_adb']]['overall_prg'])
                    time.sleep(0.5)
                    cur_progress=motor.move(cur_progress, prg_data[cur_data['most_recent_adb']]['overall_prg'])
                    rct_listen = cur_data['most_recent_adb']
                    nowFlag=1
                   

                if rct_listen != cur_data['most_recent_adb']:
                    epaper.changePIL(p.name, cur_data['most_recent_adb'])
                    rct_listen=cur_data['most_recent_adb']
                    time.sleep(0.5)
                    cur_progress=motor.move(cur_progress, prg_data[cur_data['most_recent_adb']]['overall_prg'])
                else:
                    if allFlag != 1:
                        if cur_progress!=prg_data[cur_data['most_recent_adb']]['overall_prg']:
                            cur_progress=motor.move(cur_progress, prg_data[cur_data['most_recent_adb']]['overall_prg'])
                if b.read('sb') == True:
                    print('Ongoing_All ', onNum)
                    if allFlag==0:
                        allCount=0
                        allFlag=1
                    else:
                        allCount=150
                        time.sleep(1)
                        allCount=0
                    time.sleep(0.3)
                    epaper.changePIL(p.name, cur_lists[onNum])
                    time.sleep(0.5)
                    log.Log(p.name, 'Ongoing_All', cur_lists[onNum], prg_data[cur_lists[onNum]]['overall_prg'])
                    time.sleep(0.5) 
                    cur_progress=motor.move(cur_progress, prg_data[cur_lists[onNum]]['overall_prg'])
                    if cur_progress != prg_data[cur_lists[onNum]]['overall_prg']:
                        if onNum>=(len(cur_lists)-2):
                            onNum=0
                        else:
                            onNum=onNum+1
                        time.sleep(0.3)
                        epaper.changePIL(p.name, cur_lists[onNum])
                        time.sleep(0.5)
                        log.Log(p.name, 'Ongoing_All', cur_lists[onNum], prg_data[cur_lists[onNum]]['overall_prg'])
                        time.sleep(0.5)
                        cur_progress=motor.move(cur_progress, prg_data[cur_lists[onNum]]['overall_prg'])
                    
                    if onNum>=(len(cur_lists)-2):
                        onNum=0
                    else:
                        onNum=onNum+1

                    thread_OnAll()
 
            else:
                print('ShelfMode')
                log.Log(p.name, 'ShelfMode', '', '')
                ###log###
                while b.read('sh') == False:
                    if paperFlag==0:
                        epaper.changePIL(p.name, ad_lists[shelfNum])
                        if motorFlag ==0:
                            motor.Reset()
                            time.sleep(0.5)
                            thread_shelf()
                            cur_progress=0
                            motorFlag =1
                        paperFlag=1
                nowFlag=0


except KeyboardInterrupt:
        GPIO.cleanup()


