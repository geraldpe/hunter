# -*- coding: utf-8 -*-

from progress.bar import Bar 
import requests 
from bs4 import BeautifulSoup as bs 
import urllib.request as urlreq
from time import sleep
from lib.insta_tool import load_page #add .lib whenever you use it from another program

def destroy_vows(string, y_p=False):
	a = [i for i in string]
	i = 0
	while i < len(a):
		if y_p:

			if a[i] in "aeiouy" or a[i] == "y": #on regarde si la lettre est une voyelle en comptant le y	
				a.pop(i)
			else:
				i += 1
		else:
			if a[i] in "aeiou": #on regarde si la lettre est une voyelle
				a.pop(i)
			else:
				i += 1
	result = ""
	for i in a:
		result += i

	return result

def create_brics_list(infos=["oui", "non"]): #infos est une liste qui contient toutes les infos disponibles sur la personne 
	brics_list = infos

	for i in infos:
		try:
			a = int(i)
			if type(a) == int:
				break
		except:
			b = destroy_vows(i)
			if b not in brics_list:
				brics_list.append(b)

			b = destroy_vows(i, y_p=True)
			if b not in brics_list:
				brics_list.append(b)
				

	return brics_list

def glue(thing, thing2, middle=""):
	result = []
	result.append(str(thing) + middle + str(thing2))
	result.append(str(thing2) + middle + str(thing))

	return result

def take_number(brics_list):
	number = ""
	for i in range(len(brics_list)):
		try:
			number = int(brics_list[i])
			if type(number) == int:
				brics_list.pop(i)
				break
		except:
			pass
	return number

def assemble_brics(brics_list):
	
	brics_list_bis = brics_list
	symboles = [".", "_", "__", ""] #symboles utilisés en général dans les pseudos

	pseudos = []

	for midddle in symboles:
		for i in range(len(brics_list)):
			for j in range(len(brics_list_bis)):
				if brics_list[i] != brics_list_bis[j]:
					glued = glue(brics_list[i], brics_list_bis[j], middle=midddle)

					for k in glued:
						pseudos.append(k)

	
	return pseudos

def accrementations(liste, number=""):
	pseudos = []

	if number != "":
		accr = [number, "_", "__"]
		for i in liste:
			pseudos.append(i + str(accr[0]))
			pseudos.append(i + str(accr[1]))
			pseudos.append(i + str(accr[2]))
	else:
		accr = ["_", "__"]
		for i in liste:
			pseudos.append(i + str(accr[0]))
			pseudos.append(i + str(accr[1]))
	
	pseudos += liste

	return pseudos

def pseudos_tryer(pseudos):
	success = []

	bar = Bar('checking accounts', max=len(pseudos))
	for i in pseudos:

		response = load_page(i)
		if not response == 'failed':
			success.append('https://www.instagram.com/{}/'.format(i))
			response = ""
		bar.next()

	return success

def show_urls(url_list):
	url_catalog = {}
	for i in range(len(url_list)):
		url_catalog[i] = url_list[i]

	for j in url_catalog:
		sleep(0.1)
		print(j, ":", url_catalog[j])


def main():
	brics_list = create_brics_list(["jade", "lapeyre", "12"])
	number = take_number(brics_list)
	base = assemble_brics(brics_list)
	pseudos = accrementations(base, number)

	pseudos_tryer(pseudos)

if __name__ == "__main__":
	page = load_page('jade.lpyr')
	print(page)
	#main()