import os
import sys
import argparse

from firesetup_code.firebaseinit import firebaseinit
from firesetup_code.authinit import authinit
from firesetup_code.helperfunctions import error, AUTH_PROVIDERS, warning

SCC = 75 #SeperatorCharacterCount

if(__name__ == '__main__'):
	parser = argparse.ArgumentParser()
	parser.add_argument('sloc', help="Source Directory", type= str)
	parser.add_argument('directory', help="Target Directory", type= str)
	parser.add_argument('mode', help="The Mode in Which FireSetup Runs", type=str)
	parser.add_argument('--providers', '-p', help="The Authentication Providers you want to use", default="[]")
	#Flags
	parser.add_argument('-a', action='store_true', help="Enable Setup for the Android Platform")
	parser.add_argument('-i', action='store_true', help="Enable Setup for the iOS Platform")
	parser.add_argument('-w', action='store_true', help="Enable Setup for the Web Platform")
	parser.add_argument('-all', action='store_true', help="Enable Support for all AuthProviders")


	args = parser.parse_args()

	#Get Arguments
	sloc = f"{args.sloc}/source"
	directory = args.directory
	mode = args.mode

	platforms = {
		"android": args.a,
		"ios": args.i,
		"web": args.w,
		"universal": ((not args.a and not args.i and not args.w) or (args.a and args.i and args.w))
	}

	if(mode == 'firebase'):
		firebaseinit(source=sloc, target=directory, platforms=platforms)
	elif(mode == 'auth'):
		authproviders = ("[ALL]" if args.all else args.providers)
		authinit(source=sloc, target=directory, providers=authproviders, platforms=platforms)
	else:
		print(error("Invalid Mode for FireSetup"))






	