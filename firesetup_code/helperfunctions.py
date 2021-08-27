import os
import sys

def flutter_dircheck(directory):
	directory = directory.replace('/', '\\').replace('\\', '//')
	pubspec_check = os.path.exists(os.path.join(directory, 'pubspec.yaml'))
	android_check = os.path.exists(os.path.join(directory, 'android'))
	main_dart_check = os.path.exists(os.path.join(directory, 'lib', 'main.dart'))
	return (pubspec_check and android_check and main_dart_check)


def get_platforms_missing_google_service(targetdir, platforms):
	directory = targetdir
	error_platforms = []
	if(platforms['android'] or platforms['universal']):
		if(not os.path.exists(os.path.join(directory, 'android', 'app', 'google-services.json'))):
			error_platforms.append('android')
	if(platforms['ios'] or platforms['universal']):
		if(not os.path.exists(os.path.join(directory, 'ios', 'Runner', 'GoogleService-Info.plist'))):
			error_platforms.append('ios')
	return error_platforms
		

def firesetup_usecheck(target, platform):
	if(platform == 'android'):
		with open(os.path.join(target, 'android', 'app', 'build.gradle')) as x:
			src = x.read()
			if("implementation platform('com.google.firebase:firebase-bom:27.1.0')" in src):
				return True
	if(platform == 'ios'):
		pbxproj_location = os.path.join(target, 'ios', 'Runner.xcodeproj', 'project.pbxproj')
		with open(pbxproj_location) as f:
			src = f.read()
			if('IPHONEOS_DEPLOYMENT_TARGET = 12.1' in src):
				return True
	if(platform == 'web'):
		with open(os.path.join(target, 'web', 'index.html')) as f:
			src = f.read()
			if('firebase.initializeApp(firebaseConfig);' in src):
				return True
	return False


def authprovider_setupcheck(target, platform, data):
	if(platform == 'android'):
		with open(os.path.join(target, 'android', 'app', 'src', 'main', 'AndroidManifest.xml')) as f:
			src = f.read()
			if('android.permission.INTERNET' in src):
				return True
			if('android:name="com.facebook.sdk.ApplicationId"' in src):
				return True
	if(platform == 'ios'):
		revcid = data.get('revcid')
		with open(os.path.join(target, 'ios', 'Runner', 'Info.plist')) as f:
			src = f.read()
			if(f'<string>{revcid}</string>' in src):
				return True
	if(platform == 'web'):
		with open(os.path.join(target, 'web', 'index.html')) as f:
			src = f.read()
			if('GCLIENTID' not in src):
				return True
	return False
		
		


def success(s): return f"\033[92m{s}\033[00m" #Colors the text green
def error(s): return f"\033[91m{s}\033[00m" #Colors the text red
def info(s): return f"\033[96m{s}\033[00m" #Colors the text cyan
def warning(s): return f"\033[93m{s}\033[00m" #Colors the text yelllow
def underline(s): return f"\033[4m{s}\033[00m" #Adds an underline	
def header(s): return f"\033[94m{s}\033[00m" #Purple coloured line

def get_platform_string(pDict):
	platforms = []
	platform_string = ""
	if(pDict['universal']): platform_string = "Android, iOS & Web"
	else:
		if(pDict['android']): platforms.append('Android'),
		if(pDict['ios']): platforms.append('iOS')
		if(pDict['web']): platforms.append('Web')
		if(len(platforms) == 1):
			platform_string = platforms[0]
		elif(len(platforms) == 2):
			platform_string = f"{platforms[0]} & {platforms[1]}"
		else:
			platform_string = f"{', '.join(platforms[:-1])} & {platforms[-1]}"
	return platform_string

def get_provider_string(pDict):
	providers = ['Email', 'Anonymous', 'OAuth2', 'Google']
	provider_string = ""
	if(pDict != {}):
		if(pDict['facebook']): providers.append('Facebook')
	if(len(providers) == 1):
		provider_string = providers[0]
	elif(len(providers) == 2):
		provider_string = f"{providers[0]} & {providers[1]}"
	else:
		provider_string = f"{', '.join(providers[:-1])} & {providers[-1]}"
	return provider_string


def is_macos():
	return sys.platform == 'darwin'


AUTH_PROVIDERS = ['Facebook']