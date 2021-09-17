import time
import boto3
import json
import os
import pi_participants_info as ptc

s3 = boto3.client('s3')
bucket_name = 'audiobook-rgodragon'


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
            print('Error: Creating directory ', directory)


def getData(participant):
    try:
        p=ptc.participant(participant)

        createFolder(p.directory)
        
        s3.download_file(bucket_name, p.s3_filename, p.filename)
        
        time.sleep(0.1)
        s3.download_file(bucket_name, p.s3_finished_info_name, p.finished_info_name)
        time.sleep(0.1)
        #s3.download_file(bucket_name, p.s3_log_filename, p.log_filename)
        #time.sleep(0.1)
        s3.download_file(bucket_name, p.s3_cur_filename, p.cur_filename)
        time.sleep(0.1)
        s3.download_file(bucket_name, p.s3_prg_filename, p.prg_filename)
        time.sleep(0.1)

        createFolder(p.directoryIMG)

        with open(p.filename, 'r') as f:
            basic_data=json.load(f)
                 
        ad_lists = list(basic_data)
        #print(ad_lists)
        if len(ad_lists) == 0:
            print('%s has no audiobook'%p.name)
        else: 
            for i in range (0, len(ad_lists)):
                keyIMG = '%s/%s_img/%s_%s.png'%(p.name, p.name, p.name, ad_lists[i])
                s3.download_file(bucket_name, keyIMG, '%s/%s_%s.png'%(p.directoryIMG, p.name, ad_lists[i]))
                time.sleep(0.2)
            #print('%s data is updated'%p.name)
            
    except:
        print('Failed to get s3')


#getData('p9')
