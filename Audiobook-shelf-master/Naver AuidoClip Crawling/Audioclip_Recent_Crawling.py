from selenium import webdriver
from datetime import datetime 
import time
import boto3
import json
import participants_info as ptc


debug_mode=False

s3 = boto3.client('s3')	
bucket_name = 'audiobook-rgodragon'

#로그인
login_page = 'https://nid.naver.com/nidlogin.login?url=https://audioclip.naver.com/my/audiobooks'

#최근 들은 관련 css"
ad_recent_main = 'https://audioclip.naver.com'
my_main = 'https://audioclip.naver.com/my/audiobooks'

css_recent_lists = '#content .listed_item, .type_audiobook'
css_recent_title = '.detail, .detail_text'
css_recent_progress = '.seekbar_thumb_play'
#css_recent_title = '.detail_title'

css_cur_lists = '#audiobooks .list_item.is_played'
css_all_lists = '#audiobooks .list_item, .is_played'
css_fin_lists = '#audiobooks .list_item:not(.is_played)'

css_cur_title = '.audiobook_title'
css_cur_prg = '.seekbar_thumb_play'
css_cur_chp = '.detail_chapter .chapter'


# 마이 페이지 접속 및 로그인'
			
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")


#driver = webdriver.Chrome('/Users/ipd/crawling/chrome/chromedriver', options=options)
driver = webdriver.Chrome('/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/chrome/chromedriver')
driver.implicitly_wait(3)

'''

driver2 = webdriver.Chrome('/Users/ipd/crawling/chrome/chromedriver')
driver2.implicitly_wait(3)

driver3 = webdriver.Chrome('/Users/ipd/crawling/chrome/chromedriver')
driver3.implicitly_wait(3)

'''

def P1_Crawling_Recent(participant):

	p=ptc.participant(participant)

	driver.get(my_main)
	time.sleep(3)
	print(driver.current_url)

	if driver.current_url == login_page :

		driver.execute_script("document.getElementsByName('id')[0].value=\'" + p.id + "\'")
		time.sleep(1)
		driver.execute_script("document.getElementsByName('pw')[0].value=\'" + p.pw + "\'")
		time.sleep(1)
		driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
		time.sleep(5)

	# 오디오북 청취중인 현재 챕터와 진행량
	elems = driver.find_elements_by_css_selector(css_cur_lists)
	dict_prg={}

	for elem in elems:
		try:

			elem_title=elem.find_element_by_css_selector(css_cur_title).text
			elem_prg=int(round(float(elem.find_element_by_css_selector(css_cur_prg).text.lstrip('진행률 ')),0))
			elem_chp=elem.find_element_by_css_selector(css_cur_chp).text.rstrip('.')
			elem_chp=elem_chp.rstrip()

			dict_prg[elem_title]={'current_chapter':elem_chp, 'current_chapter_progress':elem_prg}		
		except:
			continue

	# 전체 데이터 불러오기_basic_data

	with open(p.filename, 'r') as f:
		basic_data=json.load(f)

	with open(p.finished_info_name, 'r') as f:
		finished_data=json.load(f)

	ad_lists = list(basic_data)
	cur_lists = list(dict_prg)
	finished_lists = list(finished_data.keys())

	# 현재 챕터로 해당 오디오북 진행량 구하기
	for i in range(0, len(cur_lists)):
		try:
			if dict_prg[cur_lists[i]]['current_chapter'] in basic_data[cur_lists[i]]['chapter']:
				chp_title_lists=list(basic_data[cur_lists[i]]['chapter'].keys())
				chp_prg_lists=list(basic_data[cur_lists[i]]['chapter'].values())
				
				chp_order=chp_title_lists.index(dict_prg[cur_lists[i]]['current_chapter'])
				playtime= sum(chp_prg_lists)
				bf_playtime = sum(chp_prg_lists[:chp_order])

				chp_mst_rct_pgs=dict_prg[cur_lists[i]]['current_chapter_progress']/100

				#현재 챕터 진행률 * 현재 챕터 playtime
				chp_mst_rct_min=(chp_mst_rct_pgs)*(basic_data[cur_lists[i]]['chapter'][dict_prg[cur_lists[i]]['current_chapter']])
				#해당 오디오북 현재 진행률
				cur_progress=round(((chp_mst_rct_min+bf_playtime)/playtime)*100,2)
				#현재 데이터에 추가
				dict_prg[cur_lists[i]]['overall_prg']=cur_progress


				if cur_progress == 100 :
					if cur_lists[i] in finished_lists:
						print('already_exist')
					else : 
						finished_data[cur_lists[i]]='finished'
						#print(finished_data)
						with open(p.finished_info_name, 'w', encoding="utf-8") as make_file:
							json.dump(finished_data, make_file, ensure_ascii=False, indent="\t")

		except:
			print('Any book added?')
			continue

	finished_lists = list(finished_data.keys())
	# Finished 여부 판단, 이전 데이터와 개수 비교
	if len(cur_lists) != len(ad_lists) : 
		# listed 현재 챕터와 진행량
		elems = driver.find_elements_by_css_selector(css_fin_lists)
		dict_listed={}

		for elem in elems:
			try:
				elem_title=elem.find_element_by_css_selector(css_cur_title).text
				elem_chp=elem.find_element_by_css_selector(css_cur_chp).text.rstrip('.')
				elem_chp=elem_chp.rstrip()
				dict_listed[elem_title]={'current_chapter':elem_chp}

			except:
				continue
		listed_lists = list(dict_listed)


		# 다 읽은 책인지 확인하기
		for i in range(0, len(listed_lists)):
			try:
				chp_title_lists=list(basic_data[listed_lists[i]]['chapter'].keys())
				if debug_mode == True:
					print(dict_listed[listed_lists[i]]['current_chapter'], ' ', chp_title_lists[len(chp_title_lists)-1])

				if dict_listed[listed_lists[i]]['current_chapter'] == chp_title_lists[len(chp_title_lists)-1] : # 마지막 챕터 인지 확인, 다 읽은 책일때 dict_progress 에 진행량 100 추가
					dict_listed[listed_lists[i]]['overall_prg']=100
					dict_prg[listed_lists[i]]=dict_listed[listed_lists[i]]

					# 이미 다 읽은 책 일때	
					if listed_lists[i] in finished_lists: 
						print('already_exist')

					# 새롭게 다 읽은 책 일때
					else :
						finished_data[listed_lists[i]]='finished'
						print(finished_data)
						with open(p.finished_info_name, 'w', encoding="utf-8") as make_file:
							json.dump(finished_data, make_file, ensure_ascii=False, indent="\t")

						with open(p.finished_info_name, 'r') as f:
							finished=json.load(f)
							print(json.dumps(finished, ensure_ascii=False, indent="\t")) ###################
						
						print('added finished')
				# 다 읽은 책 아닐 떄_dict now에 진행률과 함께 추가해주기
				else:
					   # listed 오디오북 진행률 구하기
					for i in range(0, len(listed_lists)):
						try:
							if dict_listed[listed_lists[i]]['current_chapter'] in basic_data[listed_lists[i]]['chapter']:
								chp_title_lists=list(basic_data[listed_lists[i]]['chapter'].keys())
								chp_prg_lists=list(basic_data[listed_lists[i]]['chapter'].values())
								
								chp_order=chp_title_lists.index(dict_listed[listed_lists[i]]['current_chapter'])
								playtime= sum(chp_prg_lists)
								bf_playtime = sum(chp_prg_lists[:chp_order])

								#현재 챕터 진행률 0
								chp_mst_rct_min=0
								#해당 오디오북 현재 진행률
								cur_progress=round(((chp_mst_rct_min+bf_playtime)/playtime)*100,2)
								#현재 데이터에 추가
								dict_listed[listed_lists[i]]['overall_prg']=cur_progress
								#dict_now[listed_lists[i]]=dict_listed[listed_lists[i]]
								dict_prg[listed_lists[i]]=dict_listed[listed_lists[i]]

							else : # 새로운 오디오북이 추가된거면 
								print('new book!')
								dict_prg[listed_lists[i]]=dict_listed[listed_lists[i]]
								dict_prg[listed_lists[i]]['overall_prg']=0

						except:
							continue

					print('not finished')	
			except:
				continue

	dict_now={}
	dict_now = dict_prg.copy()

	with open(p.finished_info_name, 'r') as f:
		finished=json.load(f)
		print('--- %s finished is --- '%p.name)
		print(json.dumps(finished, ensure_ascii=False, indent="\t")) ###################

	for i in range(0, len(finished_lists)):
		try:
			del(dict_now[finished_lists[i]])
		except:
			continue

	# 가장 최근 들은 챕터와 진행량
	time.sleep(2)
	driver.get(ad_recent_main)
	time.sleep(5)
	recent_lists = driver.find_elements_by_css_selector(css_recent_lists)
	dict_recent={}

	for recent_list in recent_lists:
		try:
			recent_title=recent_list.find_element_by_css_selector(css_recent_title).text
			dict_recent[recent_title]='recently_listend'
			
		except:
			continue

	# 가장 최근 들은 오디오북 제목 및 전체 진행량 구하기
	most_recent_chp=list(dict_recent.keys())
	print('%s most_recent_chp is : '%p.name, most_recent_chp)
	try:
		if most_recent_chp[0] == '':
			print('0 is false') 
			del most_recent_chp[0]
	except IndexError:
		print("IndexError")

	for i in range(0, len(ad_lists)):
		try:

			if most_recent_chp[0] in basic_data[ad_lists[i]]['chapter']:
				dict_now['most_recent_adb']=ad_lists[i]
				if ad_lists[i] in cur_lists: 
					print('progress : ', dict_now[ad_lists[i]]['overall_prg'])
				else :
					print('It currently finished')
		except:
			dict_now['most_recent_adb']=ad_lists[i]
			continue


	# listening log 남기기
	prg_lists=list(dict_prg)

	with open(p.prg_filename, 'r') as f:
		prg_data=json.load(f)

	with open(p.log_filename, 'r') as f:
		log_data=json.load(f)

	if len(prg_lists)!= len(prg_data):
		print('new book was added')
	else :
		print('lets log')

	now = datetime.now()
	today=str(now.year)+'_'+str(now.month)+'_'+str(now.day)
	ctime=str(now.hour)+':'+str(now.minute)

	if today in dict.keys(log_data):
	    num=len(log_data[today])

	else:
		log_data[today] = []#ad_lists


	for i in range(0, len(prg_lists)) :

		try:
			if debug_mode == True:
				print(dict_prg[prg_lists[i]]['overall_prg'])
				print(prg_data[prg_lists[i]]['overall_prg'])
			
			changed_rate= (float(dict_prg[prg_lists[i]]['overall_prg'])-float(prg_data[prg_lists[i]]['overall_prg']))

			if changed_rate != 0 : 		
				listening_time=(sum(list(basic_data[prg_lists[i]]['chapter'].values()))*changed_rate)/100 # 총 챕터 재생시간 x 변화율
				listening_time=round(listening_time, 2)
				if debug_mode == True:
					print(listening_time)

				dict_log = {'listened': prg_lists[i], 'playtime': listening_time, 'progress': dict_prg[prg_lists[i]]['overall_prg'], 'time': ctime}

				log_data[today].append(dict_log)
			else :
				if debug_mode == True:
					print('no change')
		except:
			continue

	with open(p.log_filename, 'w', encoding="utf-8") as make_file:
		json.dump(log_data, make_file, ensure_ascii=False, indent="\t")

	with open(p.log_filename, 'r') as f:
		json_log=json.load(f)
		print('--- %s %s listening_log is --- '%(p.name, today))
		print(json.dumps(json_log[today], ensure_ascii=False, indent="\t"))

	s3.upload_file(p.log_filename, bucket_name, p.s3_log_filename)
	time.sleep(5)

	# 현재 데이터 파일로 저장 

	with open(p.prg_filename, 'w', encoding="utf-8") as make_file:
	    json.dump(dict_prg, make_file, ensure_ascii=False, indent="\t")

	with open(p.cur_filename, 'w', encoding="utf-8") as make_file:
	    json.dump(dict_now, make_file, ensure_ascii=False, indent="\t")


	with open(p.cur_filename, 'r') as f:
		now_data=json.load(f)
		print('--- %s dict_now is --- '%p.name)
		print(json.dumps(now_data, ensure_ascii=False, indent="\t"))

	with open(p.prg_filename, 'r') as f:
		prg_data=json.load(f)
		print('--- %s dict_prg is --- '%p.name)
		print(json.dumps(prg_data, ensure_ascii=False, indent="\t"))

	s3.upload_file(p.cur_filename, bucket_name, p.s3_cur_filename)
	time.sleep(1)

	s3.upload_file(p.prg_filename, bucket_name, p.s3_prg_filename)
	time.sleep(1)

	s3.upload_file(p.finished_info_name, bucket_name, p.s3_finished_info_name)
	time.sleep(1)


'''

def P2_Crawling_Recent(participant):

	p=ptc.participant(participant)

	driver2.get(my_main)
	time.sleep(3)
	print(driver2.current_url)

	if driver2.current_url == login_page :

		driver2.execute_script("document.getElementsByName('id')[0].value=\'" + p.id + "\'")
		time.sleep(1)
		driver2.execute_script("document.getElementsByName('pw')[0].value=\'" + p.pw + "\'")
		time.sleep(1)
		driver2.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
		time.sleep(5)

	# 오디오북 청취중인 현재 챕터와 진행량
	elems = driver2.find_elements_by_css_selector(css_cur_lists)
	dict_prg={}

	for elem in elems:
		try:

			elem_title=elem.find_element_by_css_selector(css_cur_title).text
			elem_prg=int(round(float(elem.find_element_by_css_selector(css_cur_prg).text.lstrip('진행률 ')),0))
			elem_chp=elem.find_element_by_css_selector(css_cur_chp).text.rstrip('.')
			elem_chp=elem_chp.rstrip()

			dict_prg[elem_title]={'current_chapter':elem_chp, 'current_chapter_progress':elem_prg}		
		except:
			continue

	# 전체 데이터 불러오기_basic_data

	with open(p.filename, 'r') as f:
		basic_data=json.load(f)

	with open(p.finished_info_name, 'r') as f:
		finished_data=json.load(f)

	ad_lists = list(basic_data)
	cur_lists = list(dict_prg)
	finished_lists = list(finished_data.keys())

	# 현재 챕터로 해당 오디오북 진행량 구하기
	for i in range(0, len(cur_lists)):
		try:
			if dict_prg[cur_lists[i]]['current_chapter'] in basic_data[cur_lists[i]]['chapter']:
				chp_title_lists=list(basic_data[cur_lists[i]]['chapter'].keys())
				chp_prg_lists=list(basic_data[cur_lists[i]]['chapter'].values())
				
				chp_order=chp_title_lists.index(dict_prg[cur_lists[i]]['current_chapter'])
				playtime= sum(chp_prg_lists)
				bf_playtime = sum(chp_prg_lists[:chp_order])

				chp_mst_rct_pgs=dict_prg[cur_lists[i]]['current_chapter_progress']/100

				#현재 챕터 진행률 * 현재 챕터 playtime
				chp_mst_rct_min=(chp_mst_rct_pgs)*(basic_data[cur_lists[i]]['chapter'][dict_prg[cur_lists[i]]['current_chapter']])
				#해당 오디오북 현재 진행률
				cur_progress=round(((chp_mst_rct_min+bf_playtime)/playtime)*100,2)
				#현재 데이터에 추가
				dict_prg[cur_lists[i]]['overall_prg']=cur_progress


				if cur_progress == 100 :
					if cur_lists[i] in finished_lists:
						print('already_exist')
					else : 
						finished_data[cur_lists[i]]='finished'
						#print(finished_data)
						with open(p.finished_info_name, 'w', encoding="utf-8") as make_file:
							json.dump(finished_data, make_file, ensure_ascii=False, indent="\t")

		except:
			print('Any book added?')
			continue

	finished_lists = list(finished_data.keys())
	# Finished 여부 판단, 이전 데이터와 개수 비교
	if len(cur_lists) != len(ad_lists) : 
		# listed 현재 챕터와 진행량
		elems = driver2.find_elements_by_css_selector(css_fin_lists)
		dict_listed={}

		for elem in elems:
			try:
				elem_title=elem.find_element_by_css_selector(css_cur_title).text
				elem_chp=elem.find_element_by_css_selector(css_cur_chp).text.rstrip('.')
				elem_chp=elem_chp.rstrip()
				dict_listed[elem_title]={'current_chapter':elem_chp}

			except:
				continue
		listed_lists = list(dict_listed)


		# 다 읽은 책인지 확인하기
		for i in range(0, len(listed_lists)):
			try:
				chp_title_lists=list(basic_data[listed_lists[i]]['chapter'].keys())
				if debug_mode == True:
					print(dict_listed[listed_lists[i]]['current_chapter'], ' ', chp_title_lists[len(chp_title_lists)-1])

				if dict_listed[listed_lists[i]]['current_chapter'] == chp_title_lists[len(chp_title_lists)-1] : # 마지막 챕터 인지 확인, 다 읽은 책일때 dict_progress 에 진행량 100 추가
					dict_listed[listed_lists[i]]['overall_prg']=100
					dict_prg[listed_lists[i]]=dict_listed[listed_lists[i]]

					# 이미 다 읽은 책 일때	
					if listed_lists[i] in finished_lists: 
						print('already_exist')

					# 새롭게 다 읽은 책 일때
					else :
						finished_data[listed_lists[i]]='finished'
						print(finished_data)
						with open(p.finished_info_name, 'w', encoding="utf-8") as make_file:
							json.dump(finished_data, make_file, ensure_ascii=False, indent="\t")

						with open(p.finished_info_name, 'r') as f:
							finished=json.load(f)
							print(json.dumps(finished, ensure_ascii=False, indent="\t")) ###################
						
						print('added finished')
				# 다 읽은 책 아닐 떄_dict now에 진행률과 함께 추가해주기
				else:
					   # listed 오디오북 진행률 구하기
					for i in range(0, len(listed_lists)):
						try:
							if dict_listed[listed_lists[i]]['current_chapter'] in basic_data[listed_lists[i]]['chapter']:
								chp_title_lists=list(basic_data[listed_lists[i]]['chapter'].keys())
								chp_prg_lists=list(basic_data[listed_lists[i]]['chapter'].values())
								
								chp_order=chp_title_lists.index(dict_listed[listed_lists[i]]['current_chapter'])
								playtime= sum(chp_prg_lists)
								bf_playtime = sum(chp_prg_lists[:chp_order])

								#현재 챕터 진행률 0
								chp_mst_rct_min=0
								#해당 오디오북 현재 진행률
								cur_progress=round(((chp_mst_rct_min+bf_playtime)/playtime)*100,2)
								#현재 데이터에 추가
								dict_listed[listed_lists[i]]['overall_prg']=cur_progress
								#dict_now[listed_lists[i]]=dict_listed[listed_lists[i]]
								dict_prg[listed_lists[i]]=dict_listed[listed_lists[i]]

							else : # 새로운 오디오북이 추가된거면 
								print('new book!')
								dict_prg[listed_lists[i]]=dict_listed[listed_lists[i]]
								dict_prg[listed_lists[i]]['overall_prg']=0

						except:
							continue

					print('not finished')	
			except:
				continue

	dict_now={}
	dict_now = dict_prg.copy()

	with open(p.finished_info_name, 'r') as f:
		finished=json.load(f)
		print('--- %s finished is --- '%p.name)
		print(json.dumps(finished, ensure_ascii=False, indent="\t")) ###################

	for i in range(0, len(finished_lists)):
		try:
			del(dict_now[finished_lists[i]])
		except:
			continue

	# 가장 최근 들은 챕터와 진행량
	time.sleep(2)
	driver2.get(ad_recent_main)
	time.sleep(5)
	recent_lists = driver2.find_elements_by_css_selector(css_recent_lists)
	dict_recent={}

	for recent_list in recent_lists:
		try:
			recent_title=recent_list.find_element_by_css_selector(css_recent_title).text
			dict_recent[recent_title]='recently_listend'
			
		except:
			continue

	# 가장 최근 들은 오디오북 제목 및 전체 진행량 구하기
	most_recent_chp=list(dict_recent.keys())
	print('%s most_recent_chp is : '%p.name, most_recent_chp)
	try:
		if most_recent_chp[0] == '':
			print('0 is false') 
			del most_recent_chp[0]
	except IndexError:
		print("IndexError")

	for i in range(0, len(ad_lists)):
		try:

			if most_recent_chp[0] in basic_data[ad_lists[i]]['chapter']:
				dict_now['most_recent_adb']=ad_lists[i]
				if ad_lists[i] in cur_lists: 
					print('progress : ', dict_now[ad_lists[i]]['overall_prg'])
				else :
					print('It currently finished')
		except:
			dict_now['most_recent_adb']=ad_lists[i]
			continue


	# listening log 남기기
	prg_lists=list(dict_prg)

	with open(p.prg_filename, 'r') as f:
		prg_data=json.load(f)

	with open(p.log_filename, 'r') as f:
		log_data=json.load(f)

	if len(prg_lists)!= len(prg_data):
		print('new book was added')
	else :
		print('lets log')

	now = datetime.now()
	today=str(now.year)+'_'+str(now.month)+'_'+str(now.day)
	ctime=str(now.hour)+':'+str(now.minute)

	if today in dict.keys(log_data):
	    num=len(log_data[today])

	else:
		log_data[today] = []#ad_lists


	for i in range(0, len(prg_lists)) :

		try:
			if debug_mode == True:
				print(dict_prg[prg_lists[i]]['overall_prg'])
				print(prg_data[prg_lists[i]]['overall_prg'])
			
			changed_rate= (float(dict_prg[prg_lists[i]]['overall_prg'])-float(prg_data[prg_lists[i]]['overall_prg']))

			if changed_rate != 0 : 		
				listening_time=(sum(list(basic_data[prg_lists[i]]['chapter'].values()))*changed_rate)/100 # 총 챕터 재생시간 x 변화율
				listening_time=round(listening_time, 2)
				if debug_mode == True:
					print(listening_time)

				dict_log = {'listened': prg_lists[i], 'playtime': listening_time, 'progress': prg_data[prg_lists[i]]['overall_prg'], 'time': ctime}

				log_data[today].append(dict_log)
			else :
				if debug_mode == True:
					print('no change')
		except:
			continue

	with open(p.log_filename, 'w', encoding="utf-8") as make_file:
		json.dump(log_data, make_file, ensure_ascii=False, indent="\t")

	with open(p.log_filename, 'r') as f:
		json_log=json.load(f)
		print('--- %s %s listening_log is --- '%(p.name, today))
		print(json.dumps(json_log[today], ensure_ascii=False, indent="\t"))

	s3.upload_file(p.log_filename, bucket_name, p.s3_log_filename)
	time.sleep(5)

	# 현재 데이터 파일로 저장 

	with open(p.prg_filename, 'w', encoding="utf-8") as make_file:
	    json.dump(dict_prg, make_file, ensure_ascii=False, indent="\t")

	with open(p.cur_filename, 'w', encoding="utf-8") as make_file:
	    json.dump(dict_now, make_file, ensure_ascii=False, indent="\t")


	with open(p.cur_filename, 'r') as f:
		now_data=json.load(f)
		print('--- %s dict_now is --- '%p.name)
		print(json.dumps(now_data, ensure_ascii=False, indent="\t"))

	with open(p.prg_filename, 'r') as f:
		prg_data=json.load(f)
		print('--- %s dict_prg is --- '%p.name)
		print(json.dumps(prg_data, ensure_ascii=False, indent="\t"))

	s3.upload_file(p.cur_filename, bucket_name, p.s3_cur_filename)
	time.sleep(1)

	s3.upload_file(p.prg_filename, bucket_name, p.s3_prg_filename)
	time.sleep(1)

	s3.upload_file(p.finished_info_name, bucket_name, p.s3_finished_info_name)
	time.sleep(1)



def P3_Crawling_Recent(participant):

	p=ptc.participant(participant)

	driver3.get(my_main)
	time.sleep(3)
	print(driver3.current_url)

	if driver3.current_url == login_page :

		driver3.execute_script("document.getElementsByName('id')[0].value=\'" + p.id + "\'")
		time.sleep(1)
		driver3.execute_script("document.getElementsByName('pw')[0].value=\'" + p.pw + "\'")
		time.sleep(1)
		driver3.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
		time.sleep(5)

	# 오디오북 청취중인 현재 챕터와 진행량
	elems = driver3.find_elements_by_css_selector(css_cur_lists)
	dict_prg={}

	for elem in elems:
		try:

			elem_title=elem.find_element_by_css_selector(css_cur_title).text
			elem_prg=int(round(float(elem.find_element_by_css_selector(css_cur_prg).text.lstrip('진행률 ')),0))
			elem_chp=elem.find_element_by_css_selector(css_cur_chp).text.rstrip('.')
			elem_chp=elem_chp.rstrip()

			dict_prg[elem_title]={'current_chapter':elem_chp, 'current_chapter_progress':elem_prg}		
		except:
			continue

	# 전체 데이터 불러오기_basic_data

	with open(p.filename, 'r') as f:
		basic_data=json.load(f)

	with open(p.finished_info_name, 'r') as f:
		finished_data=json.load(f)

	ad_lists = list(basic_data)
	cur_lists = list(dict_prg)
	finished_lists = list(finished_data.keys())

	# 현재 챕터로 해당 오디오북 진행량 구하기
	for i in range(0, len(cur_lists)):
		try:
			if dict_prg[cur_lists[i]]['current_chapter'] in basic_data[cur_lists[i]]['chapter']:
				chp_title_lists=list(basic_data[cur_lists[i]]['chapter'].keys())
				chp_prg_lists=list(basic_data[cur_lists[i]]['chapter'].values())
				
				chp_order=chp_title_lists.index(dict_prg[cur_lists[i]]['current_chapter'])
				playtime= sum(chp_prg_lists)
				bf_playtime = sum(chp_prg_lists[:chp_order])

				chp_mst_rct_pgs=dict_prg[cur_lists[i]]['current_chapter_progress']/100

				#현재 챕터 진행률 * 현재 챕터 playtime
				chp_mst_rct_min=(chp_mst_rct_pgs)*(basic_data[cur_lists[i]]['chapter'][dict_prg[cur_lists[i]]['current_chapter']])
				#해당 오디오북 현재 진행률
				cur_progress=round(((chp_mst_rct_min+bf_playtime)/playtime)*100,2)
				#현재 데이터에 추가
				dict_prg[cur_lists[i]]['overall_prg']=cur_progress


				if cur_progress == 100 :
					if cur_lists[i] in finished_lists:
						print('already_exist')
					else : 
						finished_data[cur_lists[i]]='finished'
						#print(finished_data)
						with open(p.finished_info_name, 'w', encoding="utf-8") as make_file:
							json.dump(finished_data, make_file, ensure_ascii=False, indent="\t")

		except:
			print('Any book added?')
			continue

	finished_lists = list(finished_data.keys())
	# Finished 여부 판단, 이전 데이터와 개수 비교
	if len(cur_lists) != len(ad_lists) : 
		# listed 현재 챕터와 진행량
		elems = driver3.find_elements_by_css_selector(css_fin_lists)
		dict_listed={}

		for elem in elems:
			try:
				elem_title=elem.find_element_by_css_selector(css_cur_title).text
				elem_chp=elem.find_element_by_css_selector(css_cur_chp).text.rstrip('.')
				elem_chp=elem_chp.rstrip()
				dict_listed[elem_title]={'current_chapter':elem_chp}

			except:
				continue
		listed_lists = list(dict_listed)


		# 다 읽은 책인지 확인하기
		for i in range(0, len(listed_lists)):
			try:
				chp_title_lists=list(basic_data[listed_lists[i]]['chapter'].keys())
				if debug_mode == True:
					print(dict_listed[listed_lists[i]]['current_chapter'], ' ', chp_title_lists[len(chp_title_lists)-1])

				if dict_listed[listed_lists[i]]['current_chapter'] == chp_title_lists[len(chp_title_lists)-1] : # 마지막 챕터 인지 확인, 다 읽은 책일때 dict_progress 에 진행량 100 추가
					dict_listed[listed_lists[i]]['overall_prg']=100
					dict_prg[listed_lists[i]]=dict_listed[listed_lists[i]]

					# 이미 다 읽은 책 일때	
					if listed_lists[i] in finished_lists: 
						print('already_exist')

					# 새롭게 다 읽은 책 일때
					else :
						finished_data[listed_lists[i]]='finished'
						print(finished_data)
						with open(p.finished_info_name, 'w', encoding="utf-8") as make_file:
							json.dump(finished_data, make_file, ensure_ascii=False, indent="\t")

						with open(p.finished_info_name, 'r') as f:
							finished=json.load(f)
							print(json.dumps(finished, ensure_ascii=False, indent="\t")) ###################
						
						print('added finished')
				# 다 읽은 책 아닐 떄_dict now에 진행률과 함께 추가해주기
				else:
					   # listed 오디오북 진행률 구하기
					for i in range(0, len(listed_lists)):
						try:
							if dict_listed[listed_lists[i]]['current_chapter'] in basic_data[listed_lists[i]]['chapter']:
								chp_title_lists=list(basic_data[listed_lists[i]]['chapter'].keys())
								chp_prg_lists=list(basic_data[listed_lists[i]]['chapter'].values())
								
								chp_order=chp_title_lists.index(dict_listed[listed_lists[i]]['current_chapter'])
								playtime= sum(chp_prg_lists)
								bf_playtime = sum(chp_prg_lists[:chp_order])

								#현재 챕터 진행률 0
								chp_mst_rct_min=0
								#해당 오디오북 현재 진행률
								cur_progress=round(((chp_mst_rct_min+bf_playtime)/playtime)*100,2)
								#현재 데이터에 추가
								dict_listed[listed_lists[i]]['overall_prg']=cur_progress
								#dict_now[listed_lists[i]]=dict_listed[listed_lists[i]]
								dict_prg[listed_lists[i]]=dict_listed[listed_lists[i]]

							else : # 새로운 오디오북이 추가된거면 
								print('new book!')
								dict_prg[listed_lists[i]]=dict_listed[listed_lists[i]]
								dict_prg[listed_lists[i]]['overall_prg']=0

						except:
							continue

					print('not finished')	
			except:
				continue

	dict_now={}
	dict_now = dict_prg.copy()

	with open(p.finished_info_name, 'r') as f:
		finished=json.load(f)
		print('--- %s finished is --- '%p.name)
		print(json.dumps(finished, ensure_ascii=False, indent="\t")) ###################

	for i in range(0, len(finished_lists)):
		try:
			del(dict_now[finished_lists[i]])
		except:
			continue

	# 가장 최근 들은 챕터와 진행량
	time.sleep(2)
	driver3.get(ad_recent_main)
	time.sleep(5)
	recent_lists = driver3.find_elements_by_css_selector(css_recent_lists)
	dict_recent={}

	for recent_list in recent_lists:
		try:
			recent_title=recent_list.find_element_by_css_selector(css_recent_title).text
			dict_recent[recent_title]='recently_listend'
			
		except:
			continue

	# 가장 최근 들은 오디오북 제목 및 전체 진행량 구하기
	most_recent_chp=list(dict_recent.keys())
	print('%s most_recent_chp is : '%p.name, most_recent_chp)
	try:
		if most_recent_chp[0] == '':
			print('0 is false') 
			del most_recent_chp[0]
	except IndexError:
		print("IndexError")

	for i in range(0, len(ad_lists)):
		try:

			if most_recent_chp[0] in basic_data[ad_lists[i]]['chapter']:
				dict_now['most_recent_adb']=ad_lists[i]
				if ad_lists[i] in cur_lists: 
					print('progress : ', dict_now[ad_lists[i]]['overall_prg'])
				else :
					print('It currently finished')
		except:
			dict_now['most_recent_adb']=ad_lists[i]
			continue


	# listening log 남기기
	prg_lists=list(dict_prg)

	with open(p.prg_filename, 'r') as f:
		prg_data=json.load(f)

	with open(p.log_filename, 'r') as f:
		log_data=json.load(f)

	if len(prg_lists)!= len(prg_data):
		print('new book was added')
	else :
		print('lets log')

	now = datetime.now()
	today=str(now.year)+'_'+str(now.month)+'_'+str(now.day)
	ctime=str(now.hour)+':'+str(now.minute)

	if today in dict.keys(log_data):
	    num=len(log_data[today])

	else:
		log_data[today] = []#ad_lists


	for i in range(0, len(prg_lists)) :

		try:
			if debug_mode == True:
				print(dict_prg[prg_lists[i]]['overall_prg'])
				print(prg_data[prg_lists[i]]['overall_prg'])
			
			changed_rate= (float(dict_prg[prg_lists[i]]['overall_prg'])-float(prg_data[prg_lists[i]]['overall_prg']))

			if changed_rate != 0 : 		
				listening_time=(sum(list(basic_data[prg_lists[i]]['chapter'].values()))*changed_rate)/100 # 총 챕터 재생시간 x 변화율
				listening_time=round(listening_time, 2)
				if debug_mode == True:
					print(listening_time)

				dict_log = {'listened': prg_lists[i], 'playtime': listening_time, 'progress': prg_data[prg_lists[i]]['overall_prg'], 'time': ctime}

				log_data[today].append(dict_log)
			else :
				if debug_mode == True:
					print('no change')
		except:
			continue

	with open(p.log_filename, 'w', encoding="utf-8") as make_file:
		json.dump(log_data, make_file, ensure_ascii=False, indent="\t")

	with open(p.log_filename, 'r') as f:
		json_log=json.load(f)
		print('--- %s %s listening_log is --- '%(p.name, today))
		print(json.dumps(json_log[today], ensure_ascii=False, indent="\t"))

	s3.upload_file(p.log_filename, bucket_name, p.s3_log_filename)
	time.sleep(5)

	# 현재 데이터 파일로 저장 

	with open(p.prg_filename, 'w', encoding="utf-8") as make_file:
	    json.dump(dict_prg, make_file, ensure_ascii=False, indent="\t")

	with open(p.cur_filename, 'w', encoding="utf-8") as make_file:
	    json.dump(dict_now, make_file, ensure_ascii=False, indent="\t")


	with open(p.cur_filename, 'r') as f:
		now_data=json.load(f)
		print('--- %s dict_now is --- '%p.name)
		print(json.dumps(now_data, ensure_ascii=False, indent="\t"))

	with open(p.prg_filename, 'r') as f:
		prg_data=json.load(f)
		print('--- %s dict_prg is --- '%p.name)
		print(json.dumps(prg_data, ensure_ascii=False, indent="\t"))

	s3.upload_file(p.cur_filename, bucket_name, p.s3_cur_filename)
	time.sleep(1)

	s3.upload_file(p.prg_filename, bucket_name, p.s3_prg_filename)
	time.sleep(1)

	s3.upload_file(p.finished_info_name, bucket_name, p.s3_finished_info_name)
	time.sleep(1)



'''
