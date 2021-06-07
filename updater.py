from firesetup import VERSION_NUMBER
import requests
import os
import re
import argparse
import subprocess

def getRAW(path):
	URL = f"https://github.com/synapsecode/FireSetup/raw/main/{path}"
	raw_text = requests.get(URL).text
	return raw_text

def is_update_available():
	raw_md = getRAW('README.md')
	raw_fs = getRAW('firesetup.py')
	return ((f'VERSION_NUMBER = "{VERSION_NUMBER}"' not in raw_fs) and (f"({VERSION_NUMBER})" not in raw_md))

def get_version_from_readme(content):
	versioning = x = re.findall("\(\d.\d.\d\)", content)
	version = VERSION_NUMBER
	if(len(versioning) != 0):
		version = versioning[0]
	return version[1:-1]

def perform_update():
	raw_md = getRAW('README.md')
	version = get_version_from_readme(raw_md)
	print(f"Updating FireSetup from v({VERSION_NUMBER}) -> v({version})")
	subprocess.call(['git', 'pull'])
	exit()

if(__name__ == '__main__'):
	parser = argparse.ArgumentParser()
	parser.add_argument('mode', help="Updater Mode", type=str)
	args = parser.parse_args()
	mode = args.mode

	if(mode == 'update'):
		if(is_update_available()):
			print(75*'-')
			perform_update()
			print(75*'-')
	elif(mode == 'check'):
		if(is_update_available()):
			print(75*'-')
			print("FireSetup: Update is Available!")
			print("Execute the Command: 'firesetup update' to Update FireSetup")
			print(75*'-')
	else:
		print("Invalid Mode")
