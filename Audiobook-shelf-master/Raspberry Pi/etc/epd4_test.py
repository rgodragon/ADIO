#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in9d
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.WARNING)


epd = epd2in9d.EPD()
font35 = ImageFont.truetype('NanumSquareRoundB.ttf', 30)
font25 = ImageFont.truetype('NanumSquareRoundB.ttf', 25)
font18 = ImageFont.truetype('NanumSquareRoundB.ttf', 18)
font11 = ImageFont.truetype('NanumBarunGothicBold.ttf', 13)


def isblank(s):
    return bool(s and s.strip())


def dspTEST(title, author, narrator) :
    try:
        epd.init()
        epd.Clear(0xFF)
       
        x_author = 100
        y_author = 0

        x_title = 40
        y_title = 0

        # 제목, 저자, 낭독자 한글자씩
        titles = list(title)
        authors = list(author+'/'+narrator)
        

        #출력될 사이즈에 따라 좌표 잡기
        size_title=0
        for i in range(0,len(titles)):
            if isblank (titles[i]): 
                size_title = size_title+35
            else:
                size_title = size_title+10
        y_title=int((epd.height-size_title)/2) 
        #print(size_title, 'and ', y_title)


        size_author=0
        for i in range(0,len(authors)):
            if isblank (authors[i]): 
                size_author = size_author+20
            else:
                size_author = size_author+5
        y_author=int((epd.height-size_author)/2)
        #print(size_author, 'and ', y_author)

        # Drawing on the Vertical image
        Limage = Image.new('1', (epd.width, epd.height), 0)  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)
        y=0

        for i in range(0, len(authors)) :
            if isblank(authors[i]):
                draw.text((x_author, y_author+y), authors[i], font = font11, fill = 1)
                y = y+20
            else:
                draw.text((x_author, y_author+y-15), authors[i], font = font11, fill = 1)
                y = y+5

        y=0

        for i in range(0, len(titles)) :
            
            if isblank(title[i]):
                draw.text((x_title, y_title+y), titles[i], font = font35, fill = 1)
                y=y+35
            else:
                draw.text((x_title, y_title+y-30), titles[i], font = font11, fill = 1)
                y=y+10
        
        Limage=Limage.rotate(180)
        epd.display(epd.getbuffer(Limage))
        time.sleep(2)

        ''' 
        logging.info("Clear...")
        epd.Clear(0xFF)
        '''
        logging.info("Goto Sleep...")
        epd.sleep()
        
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in9d.epdconfig.module_exit()
        exit()

def dspCurrent(title, chapter, progress, prg_on) :
    try:
        epd.init()
        epd.Clear(0xFF)
       
        x_title = 100
        y_title = 0

        x_chp = 40
        y_chp = 0

        titles = list(title)
        chapters = list(chapter)

        #출력될 사이즈에 따라 좌표 잡기
        size_title=0
        for i in range(0,len(titles)):
            if isblank(titles[i]): 
                size_title = size_title+20
            else:
                size_title = size_title+5
        y_title=int((epd.height-size_title)/2) 
        #print(size_title, 'and ', y_title)


        size_chapter=0
        for i in range(0,len(chapters)):
            if isblank(chapters[i]): 
                size_chapter = size_chapter+30
            else:
                size_chapter = size_chapter+10
        y_chp=int((epd.height-size_chapter)/2)
        #print(size_chapter, 'and ', y_chp)

        # Drawing on the Vertical image
        Limage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)
        #Limage=Limage.rotate(180)
        y=0

        for i in range(0, len(chapters)) :
            if isblank(chapters[i]):
                draw.text((x_chp, y_chp+y), chapters[i], font = font25, fill = 0)
                y = y+30
            else:
                draw.text((x_chp, y_chp+y-25), chapters[i], font = font11, fill = 0)
                y = y+10

        y=0

        for i in range(0, len(titles)) :
            
            if isblank(titles[i]):
                draw.text((x_title, y_title+y), titles[i], font = font11, fill = 0)
                y=y+20
            else:
                draw.text((x_title, y_title+y-15), titles[i], font = font11, fill = 0)
                y=y+5
        
        progress = str(progress)+'%'

        if prg_on == 1:
            draw.text((80, 280), progress, font = font11, fill = 0)
        
        
        Limage=Limage.rotate(180)
        epd.display(epd.getbuffer(Limage))
        time.sleep(2)

        ''' 
        logging.info("Clear...")
        epd.Clear(0xFF)
        '''
        logging.info("Goto Sleep...")
        epd.sleep()
        
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in9d.epdconfig.module_exit()
        exit()

