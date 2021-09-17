#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

import time
from PIL import Image,ImageDraw,ImageFont,ImageTk,features
import traceback
import pi_participants_info as ptc

print(features.check('raqm'))

p=ptc.participant('p8')

font35 = ImageFont.truetype('NanumSquareRoundB.ttf', 35)
font14 = ImageFont.truetype('NanumSquareRoundB.ttf', 14)

gap =0
width=600
height=800

def isblank(s):
    return bool(s and s.strip())


def dspTEST(title, author, narrator) :
    max_len=0
    x_title=0
    x_author=0
    x_narrator=0


    num_blank=0
    num_blank2=0

    titles=title.split(' ')
    print(titles)
    for i in range(0, len(titles)):
        if max_len <= len(titles[i]):
            max_len=len(titles[i])

    #print(max_len)

    title=title.replace(' ','\n')

    author='저자  '+ author
    narrator='낭독  '+ narrator

    #author=author+' 저'
    #narrator=narrator+' 낭독'


    for i in range(0, len(author)):
        if not isblank(author[i]):
            num_blank+=1
            print('yes')

    for i in range(0, len(narrator)):
        if not isblank(narrator[i]):
            num_blank2+=1
            print('no')

    max_author=len(author)
    max_narrator=len(narrator)
    print(max_author)
    print(max_narrator)
    
    #print(title)
    Limage = Image.new('RGBA', (width, height), (0,0,0,0))  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)
    draw.rectangle((320, 58, 529, 363), fill = (0,0,0,200))
    


    x_title=486-(33*(max_len-1))
    x_author=502-(int(12*(max_author-1)))+(num_blank*4)
    x_narrator=504-(int(12*(max_narrator-1)))+(num_blank2*6)

    print(x_author, x_narrator)

    #x_author=486-(33*(max_author-1))

    #max_author = 5
    #x_author = 457 - 12*4


    #draw.text((x_title, 98), title, font = font35, fill = (255,255,255, 255), spacing=15, align="right")
    #draw.text((x_author,282), author, font = font14, fill = (255,255,255, 255), spacing=15, align="right")
    #draw.text((x_narrator,300), narrator, font = fnt14, fill = (255,255,255, 255), spacing=15, align="right")

    draw.text((420,98), title, font = font35, fill = (255,255,255, 255), spacing=15, align="right", features='rtla')
    #draw.text((457,282), author, font = font14, fill = (255,255,255, 255), spacing=15, align="right")
    #draw.text((444,300), narrator, font = font14, fill = (255,255,255, 255), spacing=15, align="right")

    #draw.text((340,98), title, font = font35, fill = (255,255,255, 255), spacing=15, align="left")
    #draw.text((340,282), author, font = font14, fill = (255,255,255, 255), spacing=15, align="left")
    #draw.text((340,310), narrator, font = font14, fill = (255,255,255, 255), spacing=15, align="left")


    basewidth = 600
    #Limage = Limage.open(imageName)
    wpercent = (basewidth/float(Limage.size[0]))
    hsize = int((float(Limage.size[1])*float(wpercent)))
    img2 = Limage.resize((basewidth,hsize), Image.ANTIALIAS)
    print(img2.size[0], img2.size[1])
    #img2=img2.crop((0,31,600,831))
    #img2.paste(im=img2, box=(130, 0))
    img2=img2.transpose(Image.ROTATE_90)



    #Limage=Limage.rotate(90, expand=False)
    img2.show()
    img2.save('%s/newimage/%s_sample.png'%(p.directoryIMG, p.name))


def blending():
    im1 = Image.open('%s/newimage/%s_퇴근길 클래식 수업R.png'%(p.directoryIMG, p.name))
    im2 = Image.open('%s/newimage/%s_sample.png'%(p.directoryIMG, p.name))

    #im2 = im2.crop((600, 0, 680, 700))
    #im1.paste(im3, (0, 0), im3)
    im1.paste(im2, (0, 0), im2)

    im1.show()
    #blended = Image.blend(im1, im2, alpha=0.5)
    #blended.show()
    im1.save('%s/newimage/%s_blended.png'%(p.directoryIMG, p.name))



#dspTEST('위저드 베이커리', '구병모 도리', '엘윈 브룩스 화이')
#dspTEST('위저드 베이커리', '구병모 도리', '엘윈 브룩스 화이트')

#dspTEST('위저드 베이커리', '구병모', '류기범')

dspTEST('퇴근길 클래식 수업', '나웅준', '')

#dspTEST('위저드 베이커리', '화이트화이트화이트', '류기범 외 3인')

#dspTEST('ipd lab', '나웅준', '나웅준')

blending()

#dspTEST('82년생\n김지영\n룰루랄라라\n김지영')

