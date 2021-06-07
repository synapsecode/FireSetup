from firesetup import VERSION_NUMBER
import requests
import os
import re
import argparse

def replace_file(path, content):
	with open(path) as f:
		old_data = f.read()
		with open(path, 'w') as x:
			x.write(content)

def getRAW(path):
	URL = f"https://github.com/synapsecode/FireSetup/raw/main/{path}"
	raw_text = requests.get(URL).text
	return raw_text

def is_update_available():
	raw_text = getRAW('README.md')
	return not (f"({VERSION_NUMBER})" in raw_text)

def perform_update(cdir):
	print("Downloading the Latest Source Files...")
	raw_main_snippet = getRAW('src/main_snippet.dart')
	raw_web_src = getRAW('src/web.html')
	raw_readme = getRAW('README.md')
	raw_fs_bat = getRAW('firesetup.bat')
	raw_fs_py = getRAW('firesetup.py')
	print("Download Complete! Installing Updates..")
	#Getting the Version Number
	versioning = x = re.findall("\(\d.\d.\d\)", raw_readme)
	version = VERSION_NUMBER
	if(len(versioning) != 0):
		version = versioning[0]

	# replace_file(os.path.join(cdir, 'src', 'main_snippet.dart'), raw_main_snippet)
	# replace_file(os.path.join(cdir, 'src', 'web.html'), raw_web_src)
	# replace_file(os.path.join(cdir, 'README.md'), raw_readme)
	# replace_file(os.path.join(cdir, 'firesetup.bat'), raw_fs_bat)
	# replace_file(os.path.join(cdir, 'firesetup.py'), raw_fs_py)
	# version = 
	print(f"Update Successful! FireSetup has been updated from version: ({VERSION_NUMBER}) to version: {version}")

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

		perform_update(cdir)
