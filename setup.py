#!/usr/bin/env python3

# Jimil Patel
# <pateljim@umich.edu>
# https://www.github.com/p4telj/
# setup.py

import argparse
import requests
import getpass
import os
import sys


token = ''
file = "~/.bash_profile"


def create_bash_profile():
	# .bash_profile is loaded on remote ssh
	# creates if doesn't exist. also adds module load gcc/6.2.0 for eecs281
	if os.path.isfile(Path(file)):
		with open(file, "ra") as f:
			exists = False
			while True:
				line = f.readline()
				if line == 'module load gcc/6.2.0' or line == 'module load gcc/6.2.0 ':
				exists = True
				break
			if not exists:
				f.write('module load gcc/6.2.0')
	else:
		with open(file, "w") as f:
			f.write('module load gcc/6.2.0')
	return


def automate():
	# update .bash_profile appropriately
	with open("~/.bash_profile")
	# git --work-tree=/GIT_DIR --git-dir=/GIT_DIR/.git pull origin master

	return


def create_repo():
	# change directory, create repository
	os.chdir(args.dir)
	# try:
	# 	os.mkdir(args.name)
	# except OSError:
	# 	print('repository directory already exists.')
	# 	sys.exit(0)
	os.chdir(os.getcwd() + '/' + args.name)

	# If 2FA, uses pre-existing OAuth token. Otherwise, creates new OAuth token
	if args.secure:
		print('Please provide an access token with full repository persmissions. \nSettings / Developer Settings / Personal Access Tokens')
		global token
		token = getpass.getpass(prompt="Access Token: ")
	else:
		pwd = getpass.getpass(prompt="Password: ")
		data = '{"scope": "repo,admin::org,admin::public_key,user,delete_repo", "note": "CAEN access."}'
		requests.post('https://api.github.com/authorizations', data=data, auth=(args.user,pwd))
		response = requests.get('https://api.github.com/authorizations', auth=(args.user, pwd))
		for k in response.json():
			if k[u'note'] == u'CAEN access.':
				global token
				token = k[u'hashed_token']
				break

	# Creates project repository
	data = '{"name": "'+args.name+'", "description": "'+args.desc+'", "private": false}'
	response = requests.post('https://api.github.com/user/repos', data=data, auth=(args.user,pwd))
	print(response.json().get(u'message', "Repository creation successful."))
	return


def handle_args():
	# handle args
	parser = argparse.ArgumentParser(description='Create repository & automate git pull.')
	parser.add_argument('-d', '--dir', required=True,
						help='full directory to house repository folder.')
	parser.add_argument('-de', '--desc', required=False,
						default='default',
						help='repository description')
	parser.add_argument('-n', '--name', required=True,
						help='repo name')
	parser.add_argument('-u', '--user', required=True,
						help='github username')
	parser.add_argument('--ssh', required=False,
						action='store_true',
						help='include arg if ssh access configured')
	parser.add_argument('--2fa', required=False,
						dest="secure",
						action='store_true',
						help='include arg if 2 factor auth configured')
	return parser.parse_args()


if __name__ == "__main__":
	args = handle_args()
	create_repo()