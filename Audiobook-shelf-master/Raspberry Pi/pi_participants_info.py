
class participant:
	name = "participant"
	def __init__(self, name):
            self.name = name

            if self.name == 'p0':
                    self.id = ''
                    self.pw = ''


            elif self.name == 'p1':

                    self.id = ' '
                    self.pw = ' '

            elif self.name == 'p2':

                    self.id = ' '
                    self.pw = ' '

            elif self.name == 'p3':
\
                    self.id = ''
                    self.pw = ''		

            elif self.name == 'p4':
        
                    self.id = ''
                    self.pw = ''		
            elif self.name == 'p5':
             
                    self.id = ''
                    self.pw = ''		

            elif self.name == 'p6':
                    #
                    self.id = ''
                    self.pw = ''		


            elif self.name == 'p8':
                    self.id = ''
                    self.pw = ''


            elif self.name == 'p9':
                    self.id = ''
                    self.pw = ''



            else:
                    print('No participant')


            self.directory = '/home/pi/git-2020-audiobook-shelf/pi/%s_json'%(self.name)
            self.directoryIMG = '/home/pi/git-2020-audiobook-shelf/pi/%s_json/%s_img'%(self.name, self.name)

            self.filename = '/home/pi/git-2020-audiobook-shelf/pi/%s_json/%s_basic_info.json' %(self.name, self.name)
            self.saved_filename = '/home/pi/git-2020-audiobook-shelf/pi/%s_json/%s_basic_saved.json' %(self.name, self.name)
            self.finished_info_name = '/home/pi/git-2020-audiobook-shelf/pi/%s_json/%s_finished_info.json'%(self.name, self.name)
            self.log_filename = '/home/pi/git-2020-audiobook-shelf/pi/%s_json/%s_listening_log.json'%(self.name, self.name)
            self.cur_filename = '/home/pi/git-2020-audiobook-shelf/pi/%s_json/%s_cur_info.json'%(self.name, self.name)
            self.prg_filename = '/home/pi/git-2020-audiobook-shelf/pi/%s_json/%s_prg_info.json'%(self.name, self.name)
            self.pilog_filename = '/home/pi/git-2020-audiobook-shelf/pi/%s_json/%s_interaction_log.json'%(self.name, self.name)
            
            self.s3_filename = '%s/%s_basic_info.json'%(self.name, self.name)
            self.s3_finished_info_name = '%s/%s_finished_info.json'%(self.name, self.name)
            self.s3_log_filename = '%s/%s_listening_log.json'%(self.name, self.name)
            self.s3_cur_filename = '%s/%s_cur_info.json'%(self.name, self.name)
            self.s3_prg_filename = '%s/%s_prg_info.json'%(self.name, self.name)
            self.s3_pilog_filename = '%s/%s_interaction_log.json'%(self.name, self.name)
