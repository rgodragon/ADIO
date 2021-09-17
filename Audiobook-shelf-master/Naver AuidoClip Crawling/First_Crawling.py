import Audioclip_Cover_Image as img
import F_Crawling_Basic as b
import F_Crawling_Recent as r


def first(participant):
	#b.First_Basic(participant)
	#img.isNewbook(participant)		
	r.First_Recent(participant)


first('p9')

