
class participant:
	name = "participant"
	def __init__(self, name):
		self.name = name

		if self.name == 'p0':
			self.id = 'id'
			self.pw = 'password'


		elif self.name == 'p1':
			self.id = 'id'
			self.pw = 'password'


		elif self.name == 'p2':
			self.id = 'id'
			self.pw = 'password'


		elif self.name == 'p3':
			self.id = 'id'
			self.pw = 'password'


		elif self.name == 'p8':
			self.id = 'id'
			self.pw = 'password'


		elif self.name == 'p9':
			self.id = 'id'
			self.pw = 'password'


		else:
			print('No participant')

		self.directory = '/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/%s_json'%(self.name)
		self.directoryIMG = '/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/%s_json/%s_img'%(self.name, self.name)
		self.directoryLOG = '/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/%s_log'%(self.name)

		self.filename = '/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/%s_json/%s_basic_info.json' %(self.name, self.name)
		self.saved_filename = '/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/%s_json/%s_basic_saved.json' %(self.name, self.name)
		self.finished_info_name = '/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/%s_json/%s_finished_info.json'%(self.name, self.name)
		self.log_filename = '/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/%s_json/%s_listening_log.json'%(self.name, self.name)
		self.cur_filename = '/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/%s_json/%s_cur_info.json'%(self.name, self.name)
		self.prg_filename = '/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/%s_json/%s_prg_info.json'%(self.name, self.name)
		self.interactionLOG_filename = '/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/%s_log/%s_interaction_log.json'%(self.name, self.name)
		self.listeningLOG_filename = '/Users/ryon/OneDrive - unist.ac.kr/Ph.D/Pyton/week2-a/%s_log/%s_listening_log.json'%(self.name, self.name)


		self.s3_filename = '%s/%s_basic_info.json'%(self.name, self.name)
		self.s3_finished_info_name = '%s/%s_finished_info.json'%(self.name, self.name)
		self.s3_log_filename = '%s/%s_listening_log.json'%(self.name, self.name)
		self.s3_cur_filename = '%s/%s_cur_info.json'%(self.name, self.name)
		self.s3_prg_filename = '%s/%s_prg_info.json'%(self.name, self.name)
		self.s3_finished_info_name = '%s/%s_finished_info.json'%(self.name, self.name)
		self.s3_interactionLOG_filename = '%s/%s_interaction_log.json'%(self.name, self.name)



