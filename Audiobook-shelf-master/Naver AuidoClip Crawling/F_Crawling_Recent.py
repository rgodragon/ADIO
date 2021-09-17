import json
import participants_info as ptc



def First_Recent(participant):

	p=ptc.participant(participant)

	log_data={}
	dict_prg={}
	dict_now={}
	finished_data={}

	with open(p.log_filename, 'w', encoding="utf-8") as make_file:
		json.dump(log_data, make_file, ensure_ascii=False, indent="\t")

	with open(p.prg_filename, 'w', encoding="utf-8") as make_file:
	    json.dump(dict_prg, make_file, ensure_ascii=False, indent="\t")

	with open(p.cur_filename, 'w', encoding="utf-8") as make_file:
	    json.dump(dict_now, make_file, ensure_ascii=False, indent="\t")

	with open(p.finished_info_name, 'w', encoding="utf-8") as make_file:
		json.dump(finished_data, make_file, ensure_ascii=False, indent="\t")

#Crawling_First('p2')
