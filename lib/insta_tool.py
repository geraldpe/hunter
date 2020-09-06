# -*- coding: utf-8 -*-

import urllib.request as urlreq
import lib.dependencies as dp
import re
from colorama import init, Fore
import os

init()
posts = 0

def load_page(username):
	url = 'https://www.instagram.com/{}/'.format(username)

	try:
		sock = urlreq.urlopen(url)
		data = sock.read()
		page = data.decode('UTF-8')
	except:
		return "failed"

	return page

def get_stats(username, page):
	global posts

	
	print("username:", username)
	
	posts = int(dp.get_info_complex('"edge_owner_to_timeline_media":{"count":', page)[:-2])
	followers = int(dp.get_info_complex('"edge_followed_by":{"count":', page)[:-3])
	following = int(dp.get_info_complex('"edge_follow":{"count":', page)[:-3])
	private = dp.get_info_complex('"is_private":', page)[:-2]

	if private == "true":
		print("is private: true")
	else:
		print("is private: false")

	print("posts:", Fore.CYAN, posts, Fore.WHITE)
	if posts != 0 and private == "false":
		index_list = [m.start() for m in re.finditer('"edge_liked_by":{"count":', page)]
		likes_list = []
		for i in index_list:
			likes_list.append(dp.get_info_by_index(i, len('"edge_liked_by":{"count":'), page)[:-3])

		likes_average = dp.average(likes_list)
		print("likes average:", Fore.CYAN, likes_average, Fore.WHITE)

		index_list = [m.start() for m in re.finditer('"edge_media_to_comment":{"count":', page)]
		comments_list = []
		for i in index_list:
			comments_list.append(dp.get_info_by_index(i, len('"edge_media_to_comment":{"count":'), page)[:-3])

		comments_average = dp.average(comments_list)
		print("comments average:", Fore.CYAN, comments_average, Fore.WHITE)
	elif posts != 0 and private == "true":
		print(Fore.RED)
		print("could not make statistics on posts because the account is private")
		print(Fore.WHITE)
	else:
		print(Fore.RED)
		print("could not make statistics on posts because there is no posts")
		print(Fore.WHITE)
	
	
	print("followers:", Fore.CYAN, followers, Fore.WHITE)
	print("following:", Fore.CYAN, following, Fore.WHITE)
	

	if posts != 0 and private == "false": 
		statsl = [posts, followers, following, private, comments_average, likes_average]
	else:
		statsl = [posts, followers, following, private]

	#print(page)
	return statsl

def get_at(page, username):
	index_list = [m.start() for m in re.finditer('@', page)]
	at_list = []
	for i in index_list:
		at_list.append(dp.get_info_by_index_end(i, len('@'), page, ',')[:-1])

	running = True
	while running:
		a = 0
		for i in range(len(at_list)):
			if username in at_list[i] or at_list[i] == 'type' or at_list[i] == 'id' or at_list[i] == 'context':
				at_list.pop(i)
				running = True
				break
			else:
				a += 1
		if a == len(at_list):
			break


	return at_list

def get_biography(page):
	biography = str(dp.get_info("biography", page)[:-1])
	result = []
	
	index_list = [m.start() for m in re.finditer(str(r'\\n'), biography)]
		
	if len(index_list) > 2:
		for i in range(len(index_list)):
			if i == 0:
				result.append(biography[:index_list[i]])
			else:
				result.append(biography[index_list[i-1]+1:index_list[i]])
	elif len(index_list) == 1:
		result.append(biography[:index_list[0]])
		result.append(biography[index_list[0]+2:])

	if index_list == []:
		result.append(biography)
	else:
		pass

	return result

def load_people_list(at_list):
	ppl_list = []
	for i in at_list:
		if i in ppl_list:
			pass
		else:
			ppl_list.append(i)

	return ppl_list

def account_presence(ppl_list, at_list):
	account_presence_list = [[i, 0] for i in ppl_list]
	for i in at_list:
		for k in range(len(account_presence_list)):
			if i in account_presence_list[k][0]:
				account_presence_list[k][1] += 1
				break
			else:
				pass

	return account_presence_list

def get_fullname(page):
	fullname = str(dp.get_info("full_name", page)[:-1])
	return fullname

def save_investigations(username, statsl, account_presence_list, biography, fullname):
	if not os.path.exists('victims/{}'.format(username)):
		os.makedirs('victims/{}'.format(username))

	infos = ["posts", "followers", "following", "private", "comments average", "likes average"]

	stats_insta = open('victims/{}/stats_insta.txt'.format(username), 'w')
	if len(statsl) != len(infos):
		statsl += ["/", "/"]

	for i in range(len(infos)):
		a = str(infos[i]) + ":" + str(statsl[i])
		stats_insta.write("\n" + a)

	stats_insta.close()

	account_presence = open('victims/{}/account_presence.txt'.format(username), 'w')

	for i in range(len(account_presence_list)):
		a = account_presence_list[i][0] + ":" + str(account_presence_list[i][1])
		account_presence.write("\n" + a)
	account_presence.close()

	biography_txt = open('victims/{}/biography.txt'.format(username), 'w')

	biography_txt.write(fullname + '\n')
	for i in biography:
		biography_txt.write('\n' + i)

	biography_txt.close()

def from_insta(username):
	page = "failed"

	try:
		page = load_page(username)
	except:
		print(Fore.RED, "unexisting instagram account", Fore.WHITE)
	statsl = get_stats(username, page)
	biography = get_biography(page)
	fullname = get_fullname(page)
	
	at_list = get_at(page, username)
	ppl_list = load_people_list(at_list)
	account_presence_list = account_presence(ppl_list, at_list)
	save_investigations(username, statsl, account_presence_list, biography, fullname)

def invest():
	page = "failed"

	while page == "failed":
		username = str(input("victim's username >> "))
		page = load_page(username)
		if page == "failed":
			print(Fore.RED, "unexisting instagram account", Fore.WHITE)

	page = load_page(username)
	print(page)


if __name__ == '__main__':
	a = input("invest ? 0/1 >> ")
	if a == 0:
		from_insta()
	else:
		invest()

