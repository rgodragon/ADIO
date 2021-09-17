import json
from datetime import datetime
import time
import pi_participants_info as ptc
import boto3
#import pi_donw_boto3 as boto3


s3=boto3.client('s3')
bucket_name = 'audiobook-rgodragon'

def Log(participant, mode, title, progress):

    p=ptc.participant(participant)
    with open(p.pilog_filename, 'r') as f:
        log_data=json.load(f)

    #print(log_data)
    now = datetime.now()
    today = str(now.year)+'_'+str(now.month)+'_'+str(now.day)
    ctime = str(now.hour)+':'+str(now.minute)

    if today in dict.keys(log_data):
        num=len(log_data[today])

    else:
        log_data[today] = []


    dict_log = {'mode' : mode, 'title' : title, 'progress':progress, 'time':ctime }
    log_data[today].append(dict_log)

    with open(p.pilog_filename, 'w', encoding="utf-8") as make_file:
        json.dump(log_data, make_file, ensure_ascii=False, indent="\t")

    #print(json.dumps(log_data,ensure_ascii=False, indent="\t"))
    s3.upload_file(p.pilog_filename, bucket_name, p.s3_pilog_filename)
    time.sleep(0.1)

    print('interaction_log is uploaded')

#Log('p8', 'Ongoing_Now', '퇴근길 클래식 수업', '30.2')
    


