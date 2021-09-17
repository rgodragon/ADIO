import urllib.request
import participants_info as ptc
import json
import os
import time
from PIL import Image, ImageDraw, ImageFont, ImageTk
import boto3


s3 = boto3.client('s3')
bucket_name = 'audiobook-rgodragon'

font35 = ImageFont.truetype('NanumSquareRoundB.ttf', 35)
font14 = ImageFont.truetype('NanumSquareRoundB.ttf', 14)

width=600
height=800

def isblank(s):
    return bool(s and s.strip())


def createFolder(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except OSError:
			print('Error: Creating directory ', directory)


def downloadImage(participant):

	p=ptc.participant(participant)

	with open(p.filename, 'r') as f:
		basic_data=json.load(f)
	 
	ad_lists = list(basic_data)

	for i in range(0, len(ad_lists)):
		try:
			img_url=basic_data[ad_lists[i]]['img_url']
			img_url=img_url.replace('https','http')
			createFolder(p.directoryIMG) 
			imageName= '%s/%s_%s.png'%(p.directoryIMG, p.name, ad_lists[i])
			urllib.request.urlretrieve(img_url, imageName)
			time.sleep(1)
			resizeImage(imageName)
			dspTEST(ad_lists[i], basic_data[ad_lists[i]]['author'],  basic_data[ad_lists[i]]['narrator'],  imageName)
			time.sleep(1)
			s3.upload_file(imageName, bucket_name, '%s/%s_img/%s_%s.png'%(p.name, p.name, p.name, ad_lists[i]))
			print('s3 uploaded')
			time.sleep(1)
		except:
			continue


def dspTEST(title, author, narrator, imageName) :

	if '(' in title and ')' in title:
		a=title.find('(')
		b=title.find(')')
		print(a, b)
		title=title[0:a]

	if len(narrator) >= 15:
		narrator=narrator[0:12] + ' 낭독'
	#del title[a:b]

	print(title)
	title=title.replace(' ','\n')

	Limage = Image.new('RGBA', (width, height), (0,0,0,0))  # 255: clear the frame
	draw = ImageDraw.Draw(Limage)
	draw.rectangle((320, 58, 529, 363), fill = (0,0,0,230))

	x_title = 517
	titleSize=draw.textsize(title, font = font35, spacing=15)
	authorSize=draw.textsize(author, font = font14, spacing=15)
	narratorSize=draw.textsize(narrator, font = font14, spacing=15)

    #오른쪽 정렬
	draw.text((x_title-titleSize[0], 98), title, font = font35, fill = (255,255,255, 255), spacing=15, align="right")
	draw.text((x_title-authorSize[0]-3,282), author, font = font14, fill = (255,255,255, 255), spacing=15, align="right")
	draw.text((x_title-narratorSize[0]-3,310), narrator, font = font14, fill = (255,255,255, 255), spacing=15, align="right")


	#resize 이미지
	basewidth = 600
	wpercent = (basewidth/float(Limage.size[0]))
	hsize = int((float(Limage.size[1])*float(wpercent)))
	img2 = Limage.resize((basewidth,hsize), Image.ANTIALIAS)
	print(img2.size[0], img2.size[1])
	img2=img2.transpose(Image.ROTATE_90)

	#img2.show()

	im1 = Image.open(imageName)
	im1.paste(img2, (0, 0), img2)
	im1.show()
	im1.save(imageName)


def resizeImage(imageName):

	basewidth = 600

	img = Image.open(imageName)
	wpercent = (basewidth/float(img.size[0]))
	hsize = int((float(img.size[1])*float(wpercent)))
	img2 = img.resize((basewidth,hsize), Image.ANTIALIAS)
	img2=img2.crop((0,31,600,831))
	img2.paste(im=img2, box=(130, 0))
	img2=img2.transpose(Image.ROTATE_90)
	#img2.show()
	img2.save(imageName)


def isNewbook(participant):

	p=ptc.participant(participant)

	with open(p.saved_filename, 'r') as f:
		saved_basic=json.load(f)
	with open(p.filename, 'r') as f:
		basic_data=json.load(f)

	sv_lists = list(saved_basic)
	ad_lists = list(basic_data)

	if len(sv_lists)!=len(ad_lists):
		downloadImage(participant)
		saved_basic=basic_data.copy()
		with open(p.saved_filename, 'w', encoding="utf-8") as make_file:
			json.dump(saved_basic, make_file, ensure_ascii=False, indent="\t")
		print('--- %s img_info is --- '%p.name)
		print('new audiobook added')
		print('image update is done')

	else :
		print('--- %s img_info is --- '%p.name)
		print('same image')



#isNewbook('p8')







