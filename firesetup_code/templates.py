def generate_fb_ios_template(fbid, fbct, project_name):
    return f"""<!--  Facebook Login Setup  -->
    <key>FacebookAppID</key>
    <string>{fbid}</string>
    <key>FacebookClientToken</key>
    <string>{fbct}</string>
    <key>FacebookDisplayName</key>
    <string>{project_name}</string>"""

def generate_ios_plist_template(revclientid, data):
    is_facebook_required = (data.get('facebook') != None)
    plist_template = f"""<key>UIViewControllerBasedStatusBarAppearance</key>
    <false/>
    <key>CFBundleURLTypes</key>
    <array>
        <dict>
            <key>CFBundleURLSchemes</key>
            <array>
                <string>{revclientid}</string>
                {
                    "<string>fb{0}</string>".format(data.get('facebook')[0])
                    if is_facebook_required else ''   
                }
            </array>
        </dict>
    </array>
    {generate_fb_ios_template(
        fbid=data.get('facebook')[0],
        fbct=data.get('facebook')[1],
        project_name=data.get('project_name') 
    ) if is_facebook_required else ''}
    """
    return plist_template


def generate_fb_secrets_file(data):
    project_name = data.get('project_name')
    fbid = data.get('fbid')

    return f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
	<string name="app_name">{project_name}</string>
	<string name="facebook_app_id">{fbid}</string>
	<string name="fb_login_protocol_scheme">fb{fbid}</string>
</resources>"""

def generate_fb_sdk_manifest():
    return '''\n        <!-- ====================FACEBOOK LOGIN SETUP====================== -->
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