from firesetup_code.helperfunctions import *


def android_setup(source, targetdir):  
    #Check if changes already made
    if(firesetup_usecheck(targetdir, 'android')):
        print(warning("  ⚠️  Firebase has already been added to the Android Project"))
    else:
        print("  Adding Firebase to Android Codebase")
        # ----------------- Update Project Level Gradle ----------------
        with open(os.path.join(targetdir, 'android', 'build.gradle')) as f:
            src = f.read()
            newsrc = src.replace(
                'classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"',
                'classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"\n\t\tclasspath \'com.google.gms:google-services:4.3.5\''
            ).replace(
                "ext.kotlin_version = '1.3.50'",
                "ext.kotlin_version = '1.4.32'"
            ) #Replacing the Kotlin Version for fireauth 0.7.0 and greater
            with open(os.path.join(targetdir, 'android', 'build.gradle'), 'w') as x:
                x.write(newsrc)
        print(success("    👉 Updated project level build.gradle"))
        #------------------ Update App Level Gradle --------------------
        with open(os.path.join(targetdir, 'android', 'app', 'build.gradle')) as f:
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
                #Changing MinimumSDKVersion to 21 & Enable multiDex
                'minSdkVersion 16', 'minSdkVersion 21\n\t\tmultiDexEnabled true'
            ).replace(
                #Applying GoogleServices
                'apply from: "$flutterRoot/packages/flutter_tools/gradle/flutter.gradle"',
                'apply from: "$flutterRoot/packages/flutter_tools/gradle/flutter.gradle"\n' + '\n'.join(gservices)
            ).replace(
                #Adding FirebaseBoM Dependencies
                'implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk7:$kotlin_version"',
                'implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk7:$kotlin_version"\n\t' + '\n\t'.join(implementations),
            )

        with open(os.path.join(targetdir, 'android', 'app', 'build.gradle'), 'w') as x:
            x.write(newsrc)
        print(success("    👉 Updated App level build.gradle"))
        #---------------- Update pubspec.yaml file ------------------
        with open(os.path.join(targetdir, 'pubspec.yaml')) as f:
            src = f.read()
            dependencies = [
                'firebase_core: ^1.2.0',
            ]
            newsrc = src.replace(
            '  flutter:\n    sdk: flutter',
            '  flutter:\n    sdk: flutter\n\n  #Firebase Dependencies\n  ' + "\n  ".join(dependencies),
            )
            with open(os.path.join(targetdir, 'pubspec.yaml'), 'w') as x:
                x.write(newsrc)
        print(success("    👉 Updated pubspec.yaml"))
        #---------------- End of Firebase Android Setup ----------------
        print(success("    🟢 Android Firebase Setup Complete!"))


def ios_setup(source, targetdir):
    #Check if changes already made
    if(firesetup_usecheck(targetdir, 'ios')):
        print(warning("  ⚠️  Firebase has already been added to the iOS Codebase"))
    else:
        print("  Adding Firebase to iOS Codebase")
        # ---------------------- Updating iOS Deployment Target ----------------
        pbxproj_location = os.path.join(targetdir, 'ios', 'Runner.xcodeproj', 'project.pbxproj')
        with open(pbxproj_location) as f:
            src = f.read()
            # Replace the iOS Deployment Target from 9 -> 12.1
            newsrc = src.replace(
                'IPHONEOS_DEPLOYMENT_TARGET = 9.0;',
                'IPHONEOS_DEPLOYMENT_TARGET = 12.1;'
            )
            with open(pbxproj_location, 'w') as x:
                x.write(newsrc)
        print(success("    👉 Updated iOS Target Version from 9.0 to 12.1"))
        # ------------------- End of Firebase iOS Setup -------------------------
        print(success("    🟢 iOS Firebase Setup Complete!"))


def web_setup(source, targetdir, project_name):
    if(firesetup_usecheck(targetdir, 'web')):
        print(warning("  ⚠️  Firebase has already been added to the Web Codebase"))
    else:
        print("  Adding Firebase to Web Codebase")
        # ----------------------- Replacing web/index.html -------------------
        with open(os.path.join(targetdir, 'web', 'index.html'), 'w+') as f:
            with open(os.path.join(source, 'web_template.html')) as g:
                x = g.read().replace('PROJECT_TITLE', project_name)
                f.write(x)
        print(success("    👉 Replaced web/index.html"))
        # ------------------- End of Firebase Web Setup -------------------------
        print(success("    🟢 Web Firebase Setup Complete!"))


def firebaseinit(source, target, platforms):
    project_name = target.split('/' if is_macos else '\\')[-1]
    platform_string = get_platform_string(platforms)

    #Check if the target is a flutter directory or not
    if(not flutter_dircheck(target)):
        print(error("  ❌ Current directory is not a flutter project"))
        return
    else:
        print(f"  Target Flutter Project: " + header(project_name))
        print(f"  Target Platforms: {header(platform_string)}")

    #Check for missing GoogleService files
    googleservice_missing_platforms = get_platforms_missing_google_service(targetdir=target, platforms=platforms)
    if('android' in googleservice_missing_platforms):
        print(warning('  ⚠️  google_services.json file not found in ./android/app'))
    if('ios' in googleservice_missing_platforms):
        print(error('  ❌ GoogleService-Info.plist file not found in ./ios/Runner'))
        return

    #Run the Setup files
    if(platforms['android'] or platforms['universal']):
        android_setup(source, target)
    if(platforms['ios'] or platforms['universal']):
        ios_setup(source, target)
    if(platforms['web'] or platforms['universal']):
        web_setup(source, target, project_name)
    print(success("  🔥 Firebase has been added to your Flutter project successfully!"))

