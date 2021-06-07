#Global Constants
VERSION_NUMBER = "0.4.0"

#Imports
import os
import sys
import argparse
import updater

SCC = 75 #SeperatorCharacterCount

#Checks if the Current Directory is a Flutter Project
def is_flutter_project(directory):
	directory = directory.replace('/', '\\').replace('\\', '//')
	#Check for pubspec.yaml file and the android folder
	pubspec_check = os.path.exists(os.path.join(directory, 'pubspec.yaml'))
	android_check = os.path.exists(os.path.join(directory, 'android'))
	# print(f"Directory: {directory} | Android: {android_check} | PubSpec: {pubspec_check} -> {(pubspec_check and android_check)}")
	return (pubspec_check and android_check)

def firesetup(directory, sourceDirectory, gclientid, project_name, enable_fireauth):
	print('\n' + SCC*'-')
	print(f"FireSetup(v{VERSION_NUMBER}) running in Firebase Setup Mode")
	print(f"Executing FireSetup on Flutter Project: '{project_name}'")
	print("Using GoogleSignInClientID:", gclientid)

	# Check if FireSetup is in a Flutter Project
	if(not is_flutter_project(directory)):
		print(SCC*'-')
		print("Fatal Error: FireSetup is not Inside a Flutter Project")
		print("Please run the FireSetup Command in a Flutter Project directory")
		print(SCC*'-')
		return
	else:
		print(SCC*'-')

	#Check if FireSetup has already been used, preventing double usage
	with open(os.path.join(directory, 'android', 'app', 'build.gradle')) as x:
		src = x.read()
		if("implementation platform('com.google.firebase:firebase-bom:27.1.0')" in src):
			print("FireSetup has already been used on this project!")
			print(SCC*'-')
			return
	#--------------------------------------------------------------------------------------------------
	with open(os.path.join(directory, 'web', 'index.html'), 'w+') as f:
		src = f.read()
		with open(os.path.join(sourceDirectory, 'web.html')) as g:
			x = g.read().replace('PROJECT_TITLE', project_name).replace('GCLIENTID', gclientid if gclientid != None else "GCLIENTID")
			f.write(x)
	print("Replaced web/index.html file")
	#--------------------------------------------------------------------------------------------------
	with open(os.path.join(directory, 'android', 'build.gradle')) as f:
		src = f.read()

		newsrc = src.replace(
			'classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"',
			'classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"\n\t\tclasspath \'com.google.gms:google-services:4.3.5\''
		)

		with open(os.path.join(directory, 'android', 'build.gradle'), 'w') as x:
			x.write(newsrc)
	print("Updated Project Level build.gradle file")
	#--------------------------------------------------------------------------------------------------
	with open(os.path.join(directory, 'android', 'app', 'build.gradle')) as f:
		src = f.read()

		implementations = [
			"implementation platform('com.google.firebase:firebase-bom:27.1.0')",
			"implementation 'com.google.firebase:firebase-analytics'",
			"implementation 'com.google.guava:listenablefuture:9999.0-empty-to-avoid-conflict-with-guava'"
		]

		gservices = [
			"apply plugin: 'com.google.gms.google-services'",
		]

		newsrc = src.replace(
			#Changing MinimumSDKVersion to 21
			'minSdkVersion 16', 'minSdkVersion 21'
		).replace(
			#Applying GoogleServices
			'apply from: "$flutterRoot/packages/flutter_tools/gradle/flutter.gradle"',
			'apply from: "$flutterRoot/packages/flutter_tools/gradle/flutter.gradle"\n' + '\n'.join(gservices)
		).replace(
			#Adding FirebaseBoM Dependencies
			'implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk7:$kotlin_version"',
			'implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk7:$kotlin_version"\n\t' + '\n\t'.join(implementations),
		)

		with open(os.path.join(directory, 'android', 'app', 'build.gradle'), 'w') as x:
			x.write(newsrc)
	print("Updated App Level build.gradle file")
	#--------------------------------------------------------------------------------------------------
	with open(os.path.join(directory, 'pubspec.yaml')) as f:
		src = f.read()
		dependencies = [
			'firebase_core: ^1.2.0',
			'firebase_auth: ^1.2.0',
			'google_sign_in: ^5.0.4',
			'provider: ^5.0.0',
		]
		newsrc = src.replace(
			'  flutter:\n    sdk: flutter',
			'  flutter:\n    sdk: flutter\n\n  #Firebase Dependencies\n  ' + "\n  ".join(dependencies),
		)
		with open(os.path.join(directory, 'pubspec.yaml'), 'w') as x:
			x.write(newsrc)
	print("Added Required Dependencies to pubspec.yaml")
	#--------------------------------------------------------------------------------------------------
	if(enable_fireauth):
		with open(os.path.join(directory, 'pubspec.yaml')) as f:
			src = f.read()
			newsrc = src.replace(
				'provider: ^5.0.0',
				'provider: ^5.0.0\n  fireauth: 0.2.0'
			)
			with open(os.path.join(directory, 'pubspec.yaml'), 'w') as x:
				x.write(newsrc)

		print("Added FireAuth as a dependency")
		with open(os.path.join(sourceDirectory, 'main_snippet.dart')) as x:
			with open(os.path.join(directory, 'lib/main.dart'), 'w') as f:
				f.write(x.read())
		print("Replaced main.dart with FireAuth Example")

	print(SCC*'-')
	print("Firebase Setup Done!")
	print(SCC*'-')
	print("Final Steps\n")
	print("1) Replace the placeholder firebaseConfig object in web/index.html")
	print("   with the one you copied from the 'Add Firebase to Web App' Operation")
	print("2) Enable the Required AuthProviders in your Firebase Auth Console")
	print("3) For Social Auth Providers and Phone Auth visit (https://bit.ly/3pvWNJR)")
	print("   and follow the instructions for whichever AuthProvider you want!")
	print("4) run the 'flutter pub get' command")
	print(SCC*'-')


def facebook_setup(directory, sourceDirectory, fbid, project_name, fbname):
	print('\n' + SCC*'-')
	print(f"FireSetup(v{VERSION_NUMBER}) running in FacebookAuth Setup Mode")
	print(f"Executing FacebookAuthSetup on Flutter Project: '{project_name}'")
	print("using FacebookAppID:", fbid)

	# Check if FireSetup is in a Flutter Project
	if(not is_flutter_project(directory)):
		print(SCC*'-')
		print("Fatal Error: FacebookAuthSetup is not Inside a Flutter Project")
		print("Please run the FireSetup Command in a Flutter Project directory")
		print(SCC*'-')
		return
	else:
		print(SCC*'-')

	#--------------------------------------------------------------------------------------------------

	content = f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
	<string name="app_name">{fbname}</string>
	<string name="facebook_app_id">{fbid}</string>
	<string name="fb_login_protocol_scheme">fb{fbid}</string>
</resources>'''

	with open(os.path.join(directory, 'android', 'app', 'src', 'main', 'res', 'values', 'strings.xml'), 'w') as f:
		f.write(content)

	print("Created a strings.xml Resource File")
	#--------------------------------------------------------------------------------------------------
	manifest_path = os.path.join(directory, 'android', 'app', 'src', 'main', 'AndroidManifest.xml')
	with open(manifest_path) as f:
		src = f.read()
		newsrc = src
		#If Doesn't already contain Internet Permission
		if('<uses-permission android:name="android.permission.INTERNET"/>' not in newsrc):
			newsrc = src.replace(
				#Add Internet Permissions
				'   <application',
				'   <uses-permission android:name="android.permission.INTERNET"/>\n   <application'
			)


		fbsdk_content = '''\n        <!-- ====================FACEBOOK LOGIN SETUP====================== -->
        <meta-data 
          android:name="com.facebook.sdk.ApplicationId" 
          android:value="@string/facebook_app_id"
        />
        <activity 
          android:name="com.facebook.FacebookActivity"
          android:configChanges= "keyboard|keyboardHidden|screenLayout|screenSize|orientation"
          android:label="@string/app_name"
        />
        <activity
          android:name="com.facebook.CustomTabActivity"
          android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="@string/fb_login_protocol_scheme" />
            </intent-filter>
        </activity>
        <!-- ====================FACEBOOK LOGIN SETUP====================== -->\n'''

		if('@string/fb_login_protocol_scheme' not in newsrc):
			newsrc = newsrc.replace(
				#Add Facebook Integration
				'    </application>',
				fbsdk_content+'    </application>'
			)
		else:
			print("Facebook Integration has already been performed!")
			print(SCC*'-')
			return

		#Saving Changes
		with open(manifest_path, 'w') as x:
				x.write(newsrc)
	print("Completed Facebook Integration with AndroidManifest.xml")
	#--------------------------------------------------------------------------------------------------

	print(SCC*'-')
	print("Facebook Setup Done!")
	print(SCC*'-')


def fireupdate(cdir):
	print(SCC*'-')
	print(f"FireSetup(v{VERSION_NUMBER}) running in Update Mode")
	print("Checking For Updates...")
	if(updater.is_update_available()):
		#Update updater.py first
		print("Update Available! Starting Update...")
		raw_updater = updater.getRAW('updater.py')
		updater.replace_file(os.path.join(cdir, 'updater.py'), raw_updater)
		print("Updated the UpdateEngine")
		print("Shifting Control from FireSetup -> UpdateEngine")
		#Close this & Hand over to updater.py
		pass
	else:
		print("No Update Available")
	print(SCC*'-')


if(__name__ == '__main__'):
	parser = argparse.ArgumentParser()
	parser.add_argument('cloc', help="Current Directory", type= str)
	parser.add_argument('directory', help="Target Directory", type= str)
	parser.add_argument('mode', help="The Mode in Which FireSetup Runs", type=str, default="FireSetup")
	parser.add_argument('--gclientid', '-gcid', help="Google Client ID", type= str)
	parser.add_argument('--enable_fireauth', '-efa', help="Add FireAuth to Project along With a Template", type= str, default="False")
	
	#Facebook Setup
	parser.add_argument('--facebook_app_id', '-fbid', help="Facebook App ID", type=str, default="")
	parser.add_argument('--facebook_app_name', '-fbname', help="Facebook App Name", type=str, default="FacebookAuthApp")

	args = parser.parse_args()

	cloc = args.cloc
	directory = args.directory
	gclientid = args.gclientid
	enable_fireauth = True if args.enable_fireauth == "True" else False
	mode = args.mode
	fbid=args.facebook_app_id
	fbname = args.facebook_app_name


	project_name = directory.split('\\')[-1]
	sourceDirectory = os.path.join(cloc, 'src')


	if(mode == "firebase"):
		#Regular FireSetup
		pass
		# firesetup(directory, sourceDirectory, gclientid, project_name, enable_fireauth)
	elif(mode == "facebook"):
		#Facebook FireSetup
		if(fbid == ""):
			print("Please Provide a FacebookAppID when running in FacebookSetup Mode")
			exit()
		# facebook_setup(directory, sourceDirectory, fbid, project_name, fbname)
	elif(mode == "update"):
		fireupdate(cloc)
	else:
		print("Invalid Mode")
