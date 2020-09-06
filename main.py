# -*- coding: utf-8 -*-

import lib.insta_tool as intool
import argparse
import lib.get_pics_insta as gpi
import lib.insta_username as inus
import requests


def get_only_biography(username): # fonction qui récupère uniquement la biographie sur le compte insta de la personne

	page = "failed"

	try:
		page = load_page(username)
	except:
		if page == "failed":
			print(Fore.RED, "unexisting instagram account", Fore.WHITE)

	biography = intool.get_biography(page)
	return biography

def create_pseudo_list():
	running = True
	args_list = []
	while running:
		a = str(input("add info (if no more infos : --nomore) >> "))
		if not a == '--nomore':
			args_list.append(a)
		else:
			if not len(args_list) < 2:
				running = False
				break
			else:
				print(Fore.RED, "there must be more than one argument", Fore.WHITE)

	brics_list = inus.create_brics_list(args_list)
	number = inus.take_number(brics_list)
	base = inus.assemble_brics(brics_list)
	pseudos = inus.accrementations(base, number)

	print(len(pseudos))

	return pseudos

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-in", "--insta", help="if you want to use the insta tools", action="store_true")
	parser.add_argument("-als", "--all_stats", help="to get all the account stats", action="store_true")
	parser.add_argument("-bio", "--biography", help="to get the account biography", action="store_true")
	parser.add_argument("-pp", "--profile_pic", help="to download the profile pic of a given account", action="store_true")
	parser.add_argument("-alp", "--all_pics", help="to get all account pics", action="store_true")
	parser.add_argument("-pseul", "--pseudo_list", help="to create a potential pseudo list from infos", action="store_true")
	parser.add_argument("-test", "--test", help="to test the pseudo list to eliminate the unexisting ones", action="store_true")
	parser.add_argument("username", help="the victim's username")
	
	args = parser.parse_args()

	print(args.username)

	if args.insta and args.all_stats:	
		print("")
		intool.from_insta(args.username)
		gpi.get_prof_pic(args.username)
		gpi.get_all_posts(args.username)
	elif args.insta and args.biography:
		print("")
		print(get_only_biography(args.username))	
	elif args.insta and args.profile_pic:
		print("")
		gpi.get_prof_pic(args.username)
	elif args.insta and args.all_pics:
		print("")
		gpi.get_all_posts(args.username)
	elif args.insta and args.pseudo_list:
		print("")
		pseudos = create_pseudo_list()
		if args.test:
			success = inus.pseudos_tryer(pseudos)
			print("\n")
			ans = input("show urls ? (y/n) >> ")

			if ans == "y":
				inus.show_urls(success)
			

if __name__ == "__main__":
	main()
