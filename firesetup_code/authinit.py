from sys import platform
from firesetup_code.helperfunctions import AUTH_PROVIDERS, authprovider_setupcheck, error, firesetup_usecheck, get_platform_string, get_provider_string, header, info, is_macos, success, warning
import re
import os
from firesetup_code.templates import generate_fb_sdk_manifest, generate_fb_secrets_file, generate_ios_plist_template

def android_auth_setup(source, target, providers, data):

    #Check for Existing Setup (Facebook)
    if(authprovider_setupcheck(target, 'android', {})):
        print(warning("⚠️  AuthProviders already implemented in the Android Codebase"))
        return

    print("Adding AuthProvider Support to Android Codebase")
    # ---------------- Generate Facebook XML Strings -------------------
    if(providers.get('facebook')):
        with open(os.path.join(target, 'android', 'app', 'src', 'main', 'res', 'values', 'strings.xml'), 'w') as f:
            content = generate_fb_secrets_file(data)
            f.write(content)
        print(success("    👉 Created a Strings.xml Resource File (Facebook)"))

    # -------------------- Add Facebook SDK To AndroidManifest -----------------
    if(providers.get('facebook')):
        manifest_path = os.path.join(target, 'android', 'app', 'src', 'main', 'AndroidManifest.xml')
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

            newsrc = newsrc.replace(
                #Add Facebook Integration
                '    </application>',
                generate_fb_sdk_manifest()+'    </application>'
            )
            #Saving Changes
            with open(manifest_path, 'w') as x:
                    x.write(newsrc)

            print(success("    👉 Added FacebookSDK to AndroidManifest"))

    #------------- End of Firebase Android AuthProvider Setup ----------------
    print(success("    🟢 Android AuthProvier Setup Complete!"))

def ios_auth_setup(source, target, providers, data):

    # ---------------------- Extracting Google Reversed Client ID ---------------
    google_service_plist_location = os.path.join(target, 'ios', 'Runner', 'GoogleService-Info.plist')
    rev_cid_regex = "<key>REVERSED_CLIENT_ID<\/key>\n\t<string>com\.googleusercontent\.apps\.\d+-\w+<\/string>"
    with open(google_service_plist_location) as f:
        src = f.read()
        rev_cid_regex = "<key>REVERSED_CLIENT_ID<\/key>\n\t<string>com\.googleusercontent\.apps\.\d+-\w+<\/string>"
        match = re.search(rev_cid_regex, src).group(0)
        reversed_client_id = match.split('\n')[1][9:-9]
        # print("reversed_client_id:", reversed_client_id)

    #Check for Existing AuthProvider Code
    if(authprovider_setupcheck(target, 'ios', {'revcid': reversed_client_id})):
        print(warning("⚠️  AuthProviders already implemented in the iOS Codebase"))
        return

    print("Adding AuthProvider Support to iOS Codebase")
    print(success("    👉 Extracted ReversedClientID from GoogleServices-Info.plist"))

    #------------------- Updating Info.plist with CFBundleURLSchemes -------------
    with open(os.path.join(target, 'ios', 'Runner', 'Info.plist')) as f:
        src = f.read()
        replaced_content = generate_ios_plist_template(reversed_client_id, data)
        newsrc = src.replace(
            '<key>UIViewControllerBasedStatusBarAppearance</key>\n\t<false/>',
            replaced_content
        )
        #Write Changes to Info.plist
        with open(os.path.join(target, 'ios', 'Runner', 'Info.plist'), 'w') as x:
            x.write(newsrc)
    print(success("    👉 Added Respective CFBundleURLSchemes to Info.plist"))
    #------------- End of Firebase iOS AuthProvider Setup ----------------
    print(success("    🟢 iOS AuthProvier Setup Complete!"))

def web_auth_setup(source, target, providers, data):

    #Check for previous use
    if(authprovider_setupcheck(target, 'web', {})):
        print(warning("⚠️  AuthProviders already implemented in the Web Codebase"))
        return

    print("Adding AuthProvider Support to Web Codebase")
    gcid = data.get('google_web')

    # ------------ Replace GoogleSignInClientID -----------------
    with open(os.path.join(source, 'web_template.html')) as f:
        src = f.read()
        newsrc = src.replace(
            'GCLIENTID',
            gcid,
        )
        with open(os.path.join(target, 'web', 'index.html'), 'w') as x:
            x.write(newsrc)
        if(gcid != None):
            print(success("    👉 Added GoogleSignInClientID to web/index.html"))
    #------------- End of Firebase Web AuthProvider Setup ----------------
    print(success("    🟢 Web AuthProvier Setup Complete!"))



def authsetup(source, target, providers, platforms, data):
    pString = get_provider_string(providers)
    platform_string = get_platform_string(platforms)
    print(f"Adding Code to enable {info(pString)} Login")
    print(f"Platform: {header(platform_string)}")

    if(platforms['android'] or platforms['universal']):
        android_auth_setup(source, target, providers, data=data)
    if(platforms['ios'] or platforms['universal']):
        ios_auth_setup(source, target, providers, data=data)
    if(platforms['web'] or platforms['universal']):
        web_auth_setup(source, target, providers, data=data)

    print(success("🔥 AuthProvider Implementation Successful!"))

    #TODO: Display the Further Instructions
    


def authinit(source, target, providers, platforms):
    def getFacebookDataFromUser():
        fbid = str(input("  🔧 Enter your FacebookAppID: "))
        fbct = str(input("  🔧 Enter your FacebookClientToken: "))
        return [fbid, fbct]

    def getGCIDFromUser():
        gcid = str(input("  🔧 Enter your GoogleSignIn Client ID: "))
        return gcid

    project_name = target.split('/' if is_macos else '\\')[-1]

    if(platforms['android'] or platforms['universal']):
        if(not firesetup_usecheck(target, 'android')):
            print(error("❌ Firebase not added to Android Project! (run 'firesetup firebase -a')"))
            return
    if(platforms['ios'] or platforms['universal']):
        if(not firesetup_usecheck(target, 'ios')):
            print(error("❌ Firebase not added to iOS Project! (run 'firesetup firebase -i')"))
            return
    if(platforms['web'] or platforms['universal']):
        if(not firesetup_usecheck(target, 'web')):
            print(error("❌ Firebase not added to Web Project! (run 'firesetup firebase -w')"))
            return
    
    if(providers == '[ALL]'): #RootMode   
        data = {
            'facebook': getFacebookDataFromUser(),
            'project_name': project_name,
            'google_web': getGCIDFromUser() if (platforms['web'] or platforms['universal']) else None
        }
        authsetup(source, target, providers={
            'google': True,
            'facebook': True,
            'oauth2': True,
        }, platforms=platforms, data=data)
        return
    elif(providers == '[]'): #BasicMode
        data = {
            'project_name': project_name,
            'google_web': getGCIDFromUser() if (platforms['web'] or platforms['universal']) else None
        }
        authsetup(source, target, providers={}, platforms=platforms, data=data)
    else:
        provider_list = providers[1: len(providers)-1].split(',')
        #Check the list
        for p in provider_list:
            if(p in ["Email", "Google", "OAuth2", "Anonymous"]):
                print(warning(f"'{p}' is a default AuthProvider"))
            elif(p not in AUTH_PROVIDERS):
                print(warning(f'Unsupported AuthProvider: {p} (ignored)'))
        providers = {
            'google': True,
            'oauth2': True,
            'facebook': ('Facebook' in provider_list or 'facebook' in provider_list),
        }
        data = {
            'project_name': project_name,
            'google_web': getGCIDFromUser() if (platforms['web'] or platforms['universal']) else None,
            'facebook': getFacebookDataFromUser() if providers.get('facebook') else None,
        }
        authsetup(source, target, providers=providers, platforms=platforms, data=data)
        

