#!/usr/bin/env python3

import argparse
import requests
import getpass
import os
import sys

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
		token = getpass.getpass(prompt="Access Token: ")
	else:
		pwd = getpass.getpass(prompt="Password: ")
		data = '{"scope": "repo,admin::org,admin::public_key,user,delete_repo", "note": "CAEN access."}'
		requests.post('https://api.github.com/authorizations', data=data, auth=(args.user,pwd))
		response = requests.get('https://api.github.com/authorizations', auth=(args.user, pwd))
		for k in response.json():
			if k[u'note'] == u'CAEN access.':
				token = k[u'hashed_token']
				break
	
	#

		data = '{"name": "'+args.name+'", "description": "'+args.desc+'", "private": false}'
		#response = requests.post('https://api.github.com/user/repos', data=data, auth=(args.user,pwd))
		#print(response.json().get(u'message', "Repository creation successful."))










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