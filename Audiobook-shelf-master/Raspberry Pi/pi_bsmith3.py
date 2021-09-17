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

    pilImage = Image.open('%s/%s_%s.png'%(p.directoryIMG, p.name, targetImage))

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
    #time.sleep(50)

'''
p=ptc.participant('p3')
basic_data=data.readBasic(p.name)
ad_lists=list(basic_data)
direction=True 


while True:

    
    for i in range(0, len(ad_lists)):
        changePIL(p.name, ad_lists[i])
        motor.SpinMotor(direction, 1000)
        direction = not direction
        time.sleep(5)
'''


