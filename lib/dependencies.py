# -*- coding: utf-8 -*-

import re

#les prochaines fonctions servent à récuperer des infos
#dans le html que l'on récupère

def get_info(info, soup):
	string = '"{}":"'.format(info)
	if string in soup:
		a = soup.index(string)
		info_index = a + len(string)

	running = True
	result = ""

	while running:
		b = soup[info_index]
		result += b
		if b == '"':
			running = False
		info_index += 1

	return result

def get_info_complex(info, soup):
	string = info
	if string in soup:
		a = soup.index(string)
		info_index = a + len(string)

	running = True
	result = ""

	while running:
		b = soup[info_index]
		result += b
		if b == '"':
			running = False
		info_index += 1

	return result

def get_info_by_index(index, len_info, soup):

	info_index = index + len_info

	running = True
	result = ""

	while running:
		b = soup[info_index]
		result += b
		if b == '"':
			running = False
		info_index += 1

	return result

def get_info_by_index_end(index, len_info, soup, end):

	info_index = index + len_info

	running = True
	result = ""

	while running:
		b = soup[info_index]
		result += b
		if b == end or b == '"' or b == ' ':
			running = False
		info_index += 1

	return result

def average(liste): #juste une fonction qui calcule la moyenne
	E = 0
	for i in liste:
		E += int(i)

	return round(E/len(liste))


# les prochaines fonctions servent à formater des urls
def replacer_insta(string_to_replace, new_string, soup):

	index_list = [m.start() for m in re.finditer(string_to_replace, str(soup))]
	index_list[0] -= 4
	index_list[1] -= 5
	index_list[2] -= 10
	for i in index_list:
		soup = str(soup[:i]) + new_string + str(soup[i+len(string_to_replace)+1:])
	return str(soup)

def replacer_insta_url_posts(string_to_replace, new_string, soup):
	index_list = [m.start() for m in re.finditer(string_to_replace, str(soup))]
	index_list[0] -= 4
	index_list[1] -= 5
	index_list[2] -= 10
	index_list[3] -= 15
	for i in index_list:
		soup = str(soup[:i]) + new_string + str(soup[i+len(string_to_replace)+1:])
	return str(soup)

def destroy_info_insta_url(soup):
	index_list = [m.start()-1 for m in re.finditer("&", str(soup))]
	index_list.append(index_list[0] + 1)
	index_list.append(index_list[0] + 1)
	index_list[1] += 1

	for i in index_list:
		soup = str(soup[:i]) + str(soup[i+1:])

	soup = soup[2:-1]
	return str(soup)

def destroy_infos_insta_url_posts(soup):
	index_list = [m.start()-1 for m in re.finditer("&", str(soup))]
	index_list.append(index_list[0] + 1)
	index_list.append(index_list[0] + 1)
	index_list[1] += 1
	index_list[3] -= 1
	for i in index_list:
		soup = str(soup[:i]) + str(soup[i+1:])

	soup = soup[2:-1]
	return str(soup)