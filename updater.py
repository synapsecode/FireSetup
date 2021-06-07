#UPDATED

from firesetup import VERSION_NUMBER
import requests
import os
import argparse


def getRAW(path):
	URL = f"https://github.com/synapsecode/FireSetup/raw/main/{path}"
	raw_text = requests.get(URL).text
	return raw_text

def is_update_available():
	raw_text = getRAW('README.md')
	return not (f"({VERSION_NUMBER})" in raw_text)

def perform_update(cdir):
	print("Performing Update")

	raw_example_snippet = getRAW('src/main_snippet.dart')
	raw_web_src = getRAW('src/web.html')
	raw_readme = getRAW('README.md')
	raw_fs_bat = getRAW('firesetup.bat')
	raw_fs_py = getRAW('firesetup.py')

	with open(os.path.join(cdir, 'src', 'main_snippet.dart'), 'w') as f:
		f.write(raw_example_snippet)

if(__name__ == '__main__'):
	parser = argparse.ArgumentParser()
	parser.add_argument('cdir', help="Current Directory", type= str)
	args = parser.parse_args()
	cdir = args.cdir

	print("Runnning Update in Path:", cdir)

	if(is_update_available()):
		print(75*'-')
		print("FireSetup: Update is Available!")
		print("Execute the Command: 'firesetup update' to Update FireSetup")
		print(75*'-')
