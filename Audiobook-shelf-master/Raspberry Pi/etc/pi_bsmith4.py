import sys
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter
from PIL import Image, ImageTk
import time
import pi_participants_info as ptc
#import pi_data as data
#import pi_stepper as motor


root = tkinter.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("800x600+%d+0" % (w - 800))
canvas = tkinter.Canvas(root,width=w,height=h)
canvas.pack()
canvas.configure(background='white')


def changePIL(participant, targetImage):

    p=ptc.participant(participant)

    pilImage = Image.open('%s/newimage/%s_%s.png'%(p.directoryIMG, p.name, targetImage))

    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)

    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(400, 300,image=image)
    root.update_idletasks()
    root.update()


p=ptc.participant('p8')
'''
basic_data=data.readBasic(p.name)
ad_lists=list(basic_data)
direction=False 
'''


while True:
    changePIL(p.name, '퇴근길 클래식 수업R')
    time.sleep(5)
    changePIL(p.name, 'blended')
    time.sleep(5)
''' 
    changePIL(p.name, '퇴근길 클래식 수업R')
    time.sleep(5)
    changePIL(p.name, '퇴근길 클래식 수업L')
    time.sleep(5)
    changePIL(p.name, '퇴근길 클래식 수업B')
    time.sleep(5)

    changePIL(p.name, '오버 더 호라이즌R')
    time.sleep(5)
    changePIL(p.name, '오버 더 호라이즌L')
    time.sleep(5)
    changePIL(p.name, '오버 더 호라이즌B')
    time.sleep(5)

    changePIL(p.name, '82년생 김지영R')
    time.sleep(5)
    changePIL(p.name, '82년생 김지영L')
    time.sleep(5)
    changePIL(p.name, '82년생 김지영B')
    time.sleep(5)

    changePIL(p.name, '위저드 베이커리R')
    time.sleep(5)
    changePIL(p.name, '위저드 베이커리L')
    time.sleep(5)
    changePIL(p.name, '위저드 베이커리B')
    time.sleep(5)

    changePIL(p.name, '샬롯의 거미줄R')
    time.sleep(5)
    changePIL(p.name, '샬롯의 거미줄L')
    time.sleep(5)
    changePIL(p.name, '샬롯의 거미줄B')
    time.sleep(5)

'''






