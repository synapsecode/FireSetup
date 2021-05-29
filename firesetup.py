import os
import sys
import argparse

def firesetup(directory, sourceDirectory, gclientid, project_name, enable_fireauth):
	print(100*'=')
	print("Flutter Firebase Setup Utility v1.0!")
	print(f"Executing FireSetup on Flutter Project: {project_name}")
	print("using googleClientID:", gclientid)
	print(100*'-')
	print("Setup Initialized")

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

		newsrc = src.replace(
			#Changing MinimumSDKVersion to 21
			'minSdkVersion 16',
			'minSdkVersion 21'
		).replace(
			#Applying GoogleServices
			'apply from: "$flutterRoot/packages/flutter_tools/gradle/flutter.gradle"',
			'apply from: "$flutterRoot/packages/flutter_tools/gradle/flutter.gradle"\napply plugin: \'com.google.gms.google-services\''
		).replace(
			#Adding FirebaseBoM Dependencies
			'implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk7:$kotlin_version"',
			'implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk7:$kotlin_version"\n\timplementation platform(\'com.google.firebase:firebase-bom:27.1.0\')\n\timplementation \'com.google.firebase:firebase-analytics\''
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
				'provider: ^5.0.0\n  fireauth: 0.0.5'
			)
			with open(os.path.join(directory, 'pubspec.yaml'), 'w') as x:
				x.write(newsrc)

		print("Added FireAuth as a dependency")
		with open(os.path.join(sourceDirectory, 'main_snippet.dart')) as x:
			with open(os.path.join(directory, 'lib/main.dart'), 'w') as f:
				f.write(x.read())
		print("Replaced main.dart with FireAuth Example")
	#--------------------------------------------------------------------------------------------------	
	print(100*'-')
	print("Firebase Setup Done!")
	print(100*'=')
	print("Final Steps")
	print("Replace the placeholder firebaseConfig object in web/index.html")
	print(" with the one you copied from Add Firebase Web App Operation")
	print("Please Enable Google Authentication in your Firebase Auth Console")
	print("run flutter pub get, write some code and then run the application")
	print(100*'=')


if(__name__ == '__main__'):
	parser = argparse.ArgumentParser()
	parser.add_argument('cloc', help="Current Directory", type= str)
	parser.add_argument('directory', help="Target Directory", type= str)
	parser.add_argument('--gclientid', '-gcid', help="Google Client ID", type= str)
	parser.add_argument('--enable_fireauth', '-efa', help="Add FireAuth to Project along With a Template", type= str, default="False")
	args = parser.parse_args()

	cloc = args.cloc
	directory = args.directory
	gclientid = args.gclientid
	enable_fireauth = True if args.enable_fireauth == "True" else False

	print(cloc)

	project_name = directory.split('\\')[-1]

	sourceDirectory = os.path.join(cloc, 'src')
	firesetup(directory, sourceDirectory, gclientid, project_name, enable_fireauth)