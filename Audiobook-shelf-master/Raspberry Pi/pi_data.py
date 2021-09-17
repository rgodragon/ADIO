#import time
import json
import os
import pi_participants_info as ptc


def readBasic(participant):
    p=ptc.participant(participant)
    #basic 데이터
    with open(p.filename, 'r') as f:
        basic_data=json.load(f)
        return basic_data

def readCur(participant):
    p=ptc.participant(participant)
    
    with open(p.cur_filename, 'r') as f:
        cur_data=json.load(f)

    cur_lists = list(cur_data)
    if len(cur_lists) == 1 and 'most_recent_adb' in cur_data: # 다 읽어서 읽는 책이 하나도 없을 때
        print('empty')
        finFlag=1
        onNum=0
        #shelfNum=0
        #index=''
    elif len(cur_lists) ==0:  # 다 읽어서 읽는 책이 하나도 없을 때
        print('empty')
        finFlag=1
        onNum=0
        #shelfNum=0
        #index=''
    else:
        if 'most_recent_adb' in cur_data: # most recent + Ongoing 1개라도  있을때
            finFlag=0
            if cur_data['most_recent_adb'] not in cur_lists: # 다 읽은 책이 most recent 일때
                cur_data['most_recent_adb']=cur_lists[0]
                onNum=cur_lists.index(cur_data['most_recent_adb'])+1
                #shelfNum=cur_lists.index(cur_data['most_recent_adb'])+1
                #index=cur_lists.index(cur_data['most_recent_adb'])
            else:
                onNum=cur_lists.index(cur_data['most_recent_adb'])+1
                if cur_lists[onNum] == 'most_recent_adb':
                    onNum=0
                #shelfNum=cur_lists.index(cur_data['most_recent_adb'])+1
                #index=cur_lists.index(cur_data['most_recent_adb'])
        else: # most recent 없고, Ongoing 1개라도 있을 때
            finFlag=0
            cur_data['most_recent_adb']=cur_lists[0]
            onNum=cur_lists.index(cur_data['most_recent_adb'])+1
            #shelfNum=cur_lists.index(cur_data['most_recent_adb'])+1
            #index=cur_lists.index(cur_data['most_recent_adb'])
    
    if cur_lists[onNum] == 'most_recent_adb':
        onNum=0
    print('onNum is ', cur_lists[onNum])
    return cur_data, finFlag, onNum #shelfNum, index

def readPrg(participant):
    
    p=ptc.participant(participant)
    #basic 데이터
    with open(p.prg_filename, 'r') as f:
        prg_data=json.load(f)
        return prg_data


