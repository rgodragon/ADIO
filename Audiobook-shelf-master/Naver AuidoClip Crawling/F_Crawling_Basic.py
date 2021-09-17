from selenium import webdriver
import time
import boto3
import json
import os
import participants_info as ptc


s3 = boto3.client('s3')
bucket_name = 'audiobook-rgodragon'


my_main = 'https://audioclip.naver.com/my/audiobooks'
xpath_chp_more = '//*[@id="audiobook"]/div[2]/div/button'
login_page = 'https://nid.naver.com/nidlogin.login?url=https://audioclip.naver.com/my/audiobooks'

css_cur_lists = '#audiobooks .list_item, .is_played'

# 오디오북 기존 정보 관련 css 선택자
css_info_content = '#content .end_header'
#css_info_url = '#content > div > section > div.end_header > div.end_audiobook_thumb > img
css_info_url = '.end_audiobook_thumb .thumb_img'
css_info_title = '.end_audiobook_info_title'
css_info_playtime = '.detail_play>span'
css_info_author = '.detail_author > span:nth-child(1)'
css_info_narrator = '.detail_author > span:nth-child(2)'

# 챕터 관련 css 선택자
css_chp_chapters = '#audiobook .end_playlist_wrap'
css_chp_num = '.end_playlist_wrap > h3 > span'
css_chp_lists= '.end_playlist_item'
css_chp_title = '.title'
css_chp_time = '.playtime'

# 마이 페이지 접속 및 로그인'
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")
#driver = webdriver.Chrome('/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/chrome/chromedriver', options=options)

#driver = webdriver.Chrome('/Users/ipd/crawling/chrome/chromedriver', options=options)
driver = webdriver.Chrome('/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/chrome/chromedriver')

driver.implicitly_wait(3)

def createFolder(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except OSError:
			print('Error: Creating directory ', directory)


def First_Basic(participant):

	p=ptc.participant(participant)
	#p=ptc.participant('%s'%participant)

	driver.get(my_main)
	time.sleep(1)
	print(driver.current_url)

	if driver.current_url == login_page :

		driver.execute_script("document.getElementsByName('id')[0].value=\'" + p.id + "\'")
		time.sleep(1)
		driver.execute_script("document.getElementsByName('pw')[0].value=\'" + p.pw + "\'")
		time.sleep(1)
		driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
		time.sleep(5)

	# 구매한 모든 오디오북 리스트 가져오기
	lists = driver.find_elements_by_css_selector(css_cur_lists)
	num=len(lists)

	dict_elem={}
	dict_chp={}

	for i in range(1, num+1):

		# 각 오디오북 상세 페이지 접속 
		driver.find_element_by_xpath('//*[@id="audiobooks"]/div[2]/div[2]/div/div[%d]'%i).click()
		time.sleep(5)

		#chapnum = driver.find_element_by_css_selector(css_chp_num).text
		#chap_lists = driver.find_elements_by_css_selector(css_chp_lists)

		chap_lists = driver.find_elements_by_css_selector(css_chp_lists)
		#print(chap_lists)
		chapnum = driver.find_element_by_css_selector(css_chp_num).text
		#print(chapnum)
			

		# 각 오디오북 챕터 개수가 맞을 때까지 더보기 클릭
		while len(chap_lists)<int(chapnum):
			driver.find_element_by_xpath(xpath_chp_more).click()
			time.sleep(1)
			chap_lists = driver.find_elements_by_css_selector(css_chp_lists)

		# 각 오디오북 기본 정보 가져오기
		elems = driver.find_elements_by_css_selector(css_info_content)
		#print(elems)

		for elem in elems:
			try:
				info_title=elem.find_element_by_css_selector(css_info_title).text
				info_author=elem.find_element_by_css_selector(css_info_author).text #.rstrip(' 저')
				info_narrator=elem.find_element_by_css_selector(css_info_narrator).text
				info_playtime=elem.find_element_by_css_selector(css_info_playtime).text
				info_img_url=elem.find_element_by_css_selector(css_info_url).get_attribute("src")
				dict_elem[info_title]={'author':info_author, 'narrator':info_narrator, 'playtime':info_playtime, 'img_url':info_img_url}
			except:
				continue

		print("----- %s -----" %info_title)
		# 각 오디오북 챕터 정보 가져오기
		chap_lists = driver.find_elements_by_css_selector(css_chp_lists)
		dict_chp={}


		for chapter in chap_lists:
			try:
				chp_title=chapter.find_element_by_css_selector(css_chp_title).text.lstrip('샘플\n')
				chp_time=chapter.find_element_by_css_selector(css_chp_time).text.lstrip('재생시간\n')
				if '샘플 5분' in chp_time :
					chp_time=chp_time.replace('샘플 5분','')
				chp_time=chp_time.rstrip('분')
				chp_time=int(chp_time)
				
				dict_chp[chp_title]=chp_time

			except:
				continue
		# 마이 페이지로 복귀
		driver.get(my_main)
		time.sleep(5)

		dict_elem[info_title]['chapter']=dict_chp


	# 오디오북 리스트 default 데이터 저장
	dict_saved={}
	createFolder(p.directory)
	with open(p.filename, 'w', encoding="utf-8") as make_file:
	    json.dump(dict_elem, make_file, ensure_ascii=False, indent="\t")

	with open(p.saved_filename, 'w', encoding="utf-8") as make_file:
	    json.dump(dict_saved, make_file, ensure_ascii=False, indent="\t")

	with open(p.filename, 'r') as f:
		json_data=json.load(f)
		print(json.dumps(json_data, ensure_ascii=False, indent="\t"))

	s3.upload_file(p.filename, bucket_name, p.s3_filename)
	time.sleep(1)
	driver.close()
		