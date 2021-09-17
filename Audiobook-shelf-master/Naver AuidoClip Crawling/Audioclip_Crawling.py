import time
import threading
import Audioclip_Basic_Crawling as basic
import Audioclip_Recent_Crawling as rct
import Audioclip_Cover_Image as img



count_p1=1
count_p2=1
count_p3=1

count_p8=1
count_p9=1

'''


def thread_p1():	
	try:
		global count_p1
		print('==============================',time.ctime(),'==============================')

		print('==============================''Thread Basic_P1''==============================')		
		basic.P1_Crawling_Basic('p1')		
		img.isNewbook('p1')		
		time.sleep(1)
		
		print('==============================''Thread Recent_P1''==============================')		
		rct.P1_Crawling_Recent('p1')
		time.sleep(1)
		print('crawling_recent count p1 : ', count_p1)

		timer1=threading.Timer(300, thread_p1)
		timer1.start()
		count_p1 += 1

	except KeyboardInterrupt:
		timer1.cancel()


def thread_p2():	
	try:
		global count_p2
		print('==============================',time.ctime(),'==============================')

		print('==============================''Thread Basic_P2''==============================')		
		basic.P2_Crawling_Basic('p2')		
		img.isNewbook('p2')		
		time.sleep(1)
		
		print('==============================''Thread Recent_P2''==============================')		
		rct.P2_Crawling_Recent('p2')
		time.sleep(1)
		print('crawling_recent count p2 : ', count_p2)

		timer2=threading.Timer(300, thread_p2)
		timer2.start()
		count_p2 += 1

	except KeyboardInterrupt:
		timer2.cancel()


def thread_p3():	
	try:
		global count_p3
		print('==============================',time.ctime(),'==============================')

		print('==============================''Thread Basic_P3''==============================')		
		basic.P1_Crawling_Basic('p3')		
		img.isNewbook('p3')		
		time.sleep(1)
		
		print('==============================''Thread Recent_P3''==============================')		
		rct.P1_Crawling_Recent('p3')
		time.sleep(1)
		print('crawling_recent count p3 : ', count_p3)

		timer3=threading.Timer(300, thread_p3)
		timer3.start()
		count_p3 += 1

	except KeyboardInterrupt:
		timer3.cancel()




def thread_p9():	
	try:
		global count_p9
		print('==============================',time.ctime(),'==============================')

		print('==============================''Thread Basic_P9''==============================')		
		basic.P1_Crawling_Basic('p9')		
		img.isNewbook('p9')		
		time.sleep(1)
		
		print('==============================''Thread Recent_P9''==============================')		
		rct.P1_Crawling_Recent('p9')
		time.sleep(1)
		print('crawling_recent count p9 : ', count_p9)

		timer9=threading.Timer(60, thread_p9)
		timer9.start()
		count_p9 += 1

	except KeyboardInterrupt:
		timer9.cancel()

'''
def thread_p8():	
	try:
		global count_p8
		print('==============================',time.ctime(),'==============================')

		print('==============================''Thread Basic_P8''==============================')		
		basic.P1_Crawling_Basic('p8')		
		img.isNewbook('p8')		
		time.sleep(1)
		
		print('==============================''Thread Recent_P8''==============================')		
		rct.P1_Crawling_Recent('p8')
		time.sleep(1)
		print('crawling_recent count p8 : ', count_p8)

		timer8=threading.Timer(60, thread_p8)
		timer8.start()
		count_p8 += 1

	except KeyboardInterrupt:
		timer8.cancel()



thread_p8()



