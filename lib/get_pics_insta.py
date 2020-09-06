# -*- coding: utf-8 -*-

import requests 
from bs4 import BeautifulSoup as bs 
import urllib.request as urlreq
import json 
import random 
import os.path 
import os
import re
from progress.bar import Bar 
import lib.dependencies as dp #preciser lib. quand on utilise ce programme via main.py
from colorama import init, Fore

init() #init de colorama

def format_url(base_url): #fonction de formatage de l'url pour la pp
	#on remplace le caractère unicode u0026 par sa traduction "&"
	if '\\u0026' in base_url:
		final_url = base_url.encode('utf-8')
		final_url.decode("unicode-escape")

		final_url = dp.replacer_insta("u0026", "&", final_url)
		final_url = dp.destroy_info_insta_url(final_url)
	try:
		return final_url
	except:
		print(Fore.RED, "the link may has not been downloaded successfully", Fore.WHITE)

def format_url_post(base_url): #fonction de formatage de l'url pour les posts
	#on remplace le caractère unicode u0026 par sa traduction "&"
	if '\\u0026' in base_url: 
		final_url = base_url.encode('utf-8')
		final_url.decode("unicode-escape")

		final_url = dp.replacer_insta_url_posts("u0026", "&", final_url)
		final_url = dp.destroy_infos_insta_url_posts(final_url)

	#on utilise un try: car si le lien ne se télécharge pas bien
	#alors final_url n'est pas défini et on a une erreur ce qui permet de renvoyer un message d'erreur personnalisé
	try: 
		return final_url
	except:
		print(Fore.RED, "the link may has not been downloaded successfully", Fore.WHITE)

def get_prof_pic(insta_username): #fonction pour récupérer la pdp d'une personne
	insta_url ='https://www.instagram.com' 

	#test de l'éxistence de la page
	response = requests.get(f"{insta_url}/{insta_username}/") 

	if response.ok: 
		html = response.text 
		bs_html = bs(html, features ="lxml") 
		bs_html = bs_html.text 
		index = bs_html.find('profile_pic_url_hd')+len('profile_pic_url_hd')
		remaining_text = bs_html[index:] 
		remaining_text_index = remaining_text.find('requested_by_viewer')-3
		string_url = remaining_text[:remaining_text_index] 
		string_url = string_url[3:]

		#ici on formate l'url
		string_url = format_url(string_url) 
		
	a = 0 #téléchargement de la pdp
	if not string_url == None:
		while True: 
			#ici on donne un nom à au fichier téléchargé
			filename = insta_username + str(a) +'.jpg'
			file_exists = os.path.isfile(filename) 

			#ici on crée un dossier pour ranger les photos
			if not os.path.exists("victims/{}/pics".format(insta_username)):
	 			os.makedirs("victims/{}/pics".format(insta_username))

	 		#et là on télécharge la pdp
			if not file_exists: 
				with open("victims/{}/pics/{}".format(insta_username, filename), 'wb+') as handle: 
					response = requests.get(string_url, stream = True) 
					if not response.ok: 
						print(response) 
					for block in response.iter_content(1024): 
						if not block: 
							break
						handle.write(block) 
			else: 
				a += 1
				continue
			break
		print("")
		print("profile pic download complete") 
	
def get_all_posts(insta_username):# fonction pour récupérer tous les posts
	#le fonctionnement de cette fonction est semblable à l'autre 
	#sauf qu'ici on va créer une liste de liens à télécharger
	url = 'https://www.instagram.com/{}/'.format(insta_username)

	try:
		sock = urlreq.urlopen(url)
		data = sock.read()
		page = data.decode('UTF-8')
	except:
		return "failed"

	index_list = [m.start() for m in re.finditer('"display_url":"', page)]

	url_list = []
	for i in index_list:
		a = dp.get_info_by_index(i, 15, page)[:-1]
		if a not in url_list:
			url_list.append(a)

	formated_url_list = []
	for i in url_list:
		formated_url_list.append(format_url_post(i))

	print("")
	bar = Bar('downloading pics', max=len(formated_url_list)) 
	for i in range(len(formated_url_list)):
		#print("downloading pic {} / {}".format(i+1, len(formated_url_list)))
		while True: 
			filename = "pic" + str(random.randint(0, 100000)) +'.jpg'
			file_exists = os.path.isfile(filename) 

			if not os.path.exists("victims/{}/pics".format(insta_username)):
	 			os.makedirs("victims/{}/pics".format(insta_username))

			if not file_exists: 
				with open("victims/{}/pics/{}".format(insta_username, filename), 'wb+') as handle: 
					response = requests.get(formated_url_list[i], stream = True) 
					if not response.ok: 
						print(response) 
					for block in response.iter_content(1024): 
						if not block: 
							break
						handle.write(block) 
			else: 
				a += 1
				continue
			break
		bar.next()
	print("\ndownload complete")


def main():

	insta_username = input('enter username of instagram : ') 
	get_prof_pic(insta_username)

if __name__ == "__main__":
	main()


