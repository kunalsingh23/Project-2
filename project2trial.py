import requests
import re
from bs4 import BeautifulSoup

string = "http://www.bbc.c is a great site and https://www.facebook.com"

#Number 1 
def url(s):

	http = re.findall('http://\S+', s)
	https = re.findall('https://\S+', s)

	lst = (http + https)


	for link in lst:
		countlink = 0
		for character in link:
			if character == '.':
				countlink += 1
		if countlink >= 1:
			pass
		else:
			lst.remove(link)

	for link in lst:
		locations = [x for x, v in enumerate(link) if v == '.']
		if (((len(link) - 1) - locations[-1]) < 2):
			lst.remove(link)


	
	return (lst)

#Number 2


def grab_headlines():
    base_url = 'https://www.michigandaily.com/section/opinion'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "lxml")
    x = (soup.find_all(class_="view view-most-read view-id-most_read view-display-id-panel_pane_1 view-dom-id-99658157999dd0ac5aa62c2b284dd266"))
    for thing in x:
        headlines = (thing.text)


    loh = headlines.split('\n')
    finallst = []

    for headline in loh:
    	if len(headline) > 1:
    		finallst.append(headline.rstrip())
   
    return (finallst)


def findnumofpages():
	base_url = 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastna me_value=&rid=All'
	r = requests.get(base_url, headers={'User-Agent': 'SI_CLASS'})
	soup = BeautifulSoup(r.text, 'lxml')

	x = soup.find_all(class_ = "pager-current")

	for thing in x:
		mekk = (thing.text)

	return (int(mekk.split()[-1]))

def findlinks():
	base_url = 'https://www.si.umich.edu/'
	justfirst = 'directory?field_person_firstname_value=&field_person_lastna me_value=&rid=All'
	alllinks = []
	upnext = []
	for x in (range(findnumofpages())):
		if x == 0:
			url = base_url + justfirst
			alllinks.append(url)
			r = requests.get(url, headers={'User-Agent': 'SI_CLASS'})
			soup = BeautifulSoup(r.text, 'lxml')

			link = (soup.find_all(class_ = "pager-next last"))
			for thing in link:
				upnext.append(thing.a['href'])

		if (x != 0):
			url = base_url + upnext[-1]
			if url[-2:] != '12':
				alllinks.append(url)
				r = requests.get(url, headers={'User-Agent': 'SI_CLASS'})
				soup = BeautifulSoup(r.text, 'lxml')
				
				link = (soup.find_all(class_ = "pager-next last"))
				for thing in link:
					upnext.append(thing.a['href'])
			else:
				alllinks.append(url)
				return (alllinks)


def get_umsi_data():
	
	listofnames = []
	listoftitles = []
	listoftuples = []

	
	for link in findlinks():
		r = requests.get(link, headers={'User-Agent': 'SI_CLASS'})
		soup = BeautifulSoup(r.text, 'lxml')
		x = (soup.find_all(class_="field field-name-title field-type-ds field-label-hidden"))
		y = (soup.find_all(class_="field field-name-field-person-titles field-type-text field-label-hidden"))

		for thing in x:
		 	listofnames.append(thing.h2.text)

		for thing in y:
			listoftitles.append(thing.text)

		for idx in (range(len(listofnames))):
			name = listofnames[idx]
			title = listoftitles[idx]
			listoftuples.append((name, title))

	umsi_titles = {}

	for tup in listoftuples:
		umsi_titles[tup[0]] = tup[1]

	return (umsi_titles)


def num_students(data):
    dictionary = data
    count = 0
    for item in dictionary.values():
    	if item == 'PhD student':
    		count += 1
    	else:
    		pass



print (num_students())




