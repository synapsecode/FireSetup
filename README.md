<img src="https://i.ibb.co/9b9sbQS/New-Project.png" align="right">


# Flutter FireSetup Utility (0.4.0)
A Simple Automated way of Adding Firebase to your flutter project! Makes the process easy as you do not need to individually go into each file and add code snippets! The script takes care of that for you!
As a bonus, you can integrate my [FireAuth](https://github.com/synapsecode/fireauth) package effortlessly by using this script.
It uses Python internally

<br>

> **🔴🔴🔴 NOTE: FireSetup Limitations**  
> As of now, FireSetup is able to add Firebase only to Android & Web Apps, You must add Firebase to iOS on your own.

## System Requirements
* Windows 10
* Python 3 (if not, please install python3)

## FireSetup OneTime Installation
* Make sure you have python installed, type python in cmd & if the python prompt opens, you can continue.
* Git Clone this Project into a folder of your choice
* cd into this folder, copy the folder path and add it to your PATH environment variable
* Close all CMD instances and reopen and now you should be able to use firesetup from anywhere on your computer.
* To Test FireSetup, open any random directory from cmd and run the command firesetup, If you see an output, that means it works!


## Steps To Use FireSetup

### 🟡 Step 1: Create a flutter project
```batch
flutter create testapp
cd testapp
```

---

### 🟡 Step 2: Create a Firebase Project (or) Open an Existing One
  Use the Firebase Console to do this! It's very straightforward
  
 ---
 
### 🟡 Step 3: Add an Android App in Firebase Console
  - Register the App
  - Save the google_services.json file in android/app
  - Click Next and do not proceed with editing any other files as This will be done by FireSetup

---

### 🟡 Step 4: Add Web App in Firebase Console
  - Register the App
  - From the code snippet provided by firebase, just copy the firebaseConfig object and save it somewhere
  - Click Next and do not proceed with editing any other files as This will be done by FireSetup
 
---

### 🟡 Step 5: Run FireSetup
  * Inside your flutter project, open cmd and enter this command (assuming you have installed FireSetup Correctly):

  ```bash
  firesetup init -gcid=YOUR_GOOGLE_SIGNIN_ID -efa=True
  ```
  
  * The **-gcid** flag is useful for GoogleSignIn on the Web
  * The **-efa** flag stands for Enable FireAuth and if true, it adds the [FireAuth](https://github.com/synapsecode/fireauth) package to pubspec.yaml and replaces your main.dart file with an example snippet of how to use FireAuth
 > The Arguements are Completely Optional

### 🟡 Step 5.1: Add firebaseConfig to Web
  - Open the flutter project using an IDE like VSCode for example
  - Go to the /web/index.html file and replace the firebaseConfig object there with the one you copied when adding the webApp

---

### 🟡 Step 6: Enable Authentication Methods
- Head over to the Authentication Section of your Firebase Project's Console
- Click on Get Started
- Go to the SignIn Method Tab
- Enable whichever Auth Provider you need!
---

### 🔵 Testing
  * Firstly, Get all the newly added packages
    ```
    flutter pub get
    ```
  * Write Some Code
  * Run the Application

    ```
    flutter run -d chrome (For Flutter Web)
    flutter run -d <device_identifier> (For Flutter Native)
    ```
    
---

## Additional Setup Instructions
Now, the basic setup is complete! You can use AnonymousSignIn and Mail SignIn directly provided you have enabled them in the Firebase Console.
To use Google SignIn, Phone SignIn and the other Social SignIn Methods, follow the Steps given in each Section!


<details><summary>🟢 Google</summary>
  
  #### A) Enable the Google AuthProvider on the Firebase Console

  #### B) Get the GoogleSignInClientID (For FlutterWeb only)
  * Go to the [Google Cloud Platform Console](https://console.cloud.google.com)
  * Login With the Same Google Account used for Firebase
  * Open the GCP Project with the same name as your firebase project
  * Search Credentials in the Search Box and click on API Credentials
  * Copy the webClientID under OAuth 2.0 Client IDs
  * Go to /web/index.html and replace the placeholder string GCLIENTID with the copied clientID!

  #### C) Add the SHA-1 and SHA-256 Keys to Firebase
  * Go to your /android folder in the flutter project, open terminal and type this:

  ```batch
   gradlew signingReport
  ```
  * now, copy the SHA1 and SHA-256 Keys and store it somewhere.
  * Go to your firebase android app's settings in the [Firebase Console](https://console.firebase.google.com/)
  * Scroll to the bottom to 'SHA certificate fingerprints'
  * Click On 'Add Fingerprint' and add both the Keys. Done!
  
---
</details>

<details><summary>🟢 Phone</summary>
  
  #### A) Enable the Phone AuthProvider on the Firebase Console and click on Save
  
  #### B) Add the SHA-1 & SHA-256 Keys (process shown in Google's Additional Setup)
  
  #### C) Remove Android ReCaptcha Verification
  * Open your GCP Project (similar way as previously done)
  * search for Android Device Verification
  * Enable the API and done!

---
</details>

<details><summary>🟢 Twitter (OAuth)</summary>

#### A) Create Twitter OAuth App
- Go to the [Twitter Developer Console](https://developer.twitter.com/en/portal/projects-and-apps)
- Scroll Down and click on Create App
- Then Enter your App Name, copy the API Key, API Secret Key and the Bearer Token and save it somewhere

#### B) Enable the TwitterSignIn AuthProvider on the Firebase Console
- Enable the Twitter SignIn Provider in the Firebase Console
- Copy the API Key & the API Secret that you saved before and paste it in the respective fields
- Copy the CallbackURL that is provided under the API Key & API Secret Fields

#### C) Enable 3-legged-OAuth
- Go to the Settings of your Twitter App on the Developer Console, Scroll Down to Authentication Settings and click on Edit
- Enable 3-legged-oauth
- Paste the previously copied callbackURL in the respective field and also pass your website link in the respective field and click on save!
- And the Twitter OAuth SignIn Setup is Done!

---
</details>

<details><summary>🟢 Github (OAuth)</summary>

#### A) Enable the Github SignIn Provider on the Firebase Console
- Keep the Dialog Open and just copy the provided callbackURL

#### B) Create Github OAuth App
- Go to the [Gitbub Developer Settings](https://github.com/settings/developers) and click on New OAuth App
- Fill in the Details and paste the previously copied CallbackURL in the respective field and submit
- Now you will be on a App Dashboard, Copy the ClientID and save it somewhere
- Click on Generate New Client Secret and save it somewhere
- Update any other required fields and click on Update Application

#### C) Final Step
- Go back to the open dialog on the Firebase Console
- Paste the ClientID & Client Secret in their respective fields and click on Save!
- And the Github OAuth SignIn Setup is Done!
  
---
</details>

<details><summary>🟢 Microsoft (OAuth)</summary>
  
#### A) Enable the Microsoft SignIn Provider on the Firebase Console
- Keep the Dialog Open and just copy the provided redirectURL
  
#### B) Create an Microsoft Azure AD Application
- Open [MSFT Azure Portal](https://portal.azure.com/) and Sign in, You will be then redirected to the Azure Homepage
- Click on the Hamburger Icon on the Left to Reveal the Sidebar and then click on 'Azure Active Directory'
- Now, Click on 'App Registrations' in the Sidebar present on that Window
- Now, Click on the 'New Registration' Button on the top and Fill in the details
- Under the 'Supported Account Types' Heading Select the Option for 'Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)'
- Under the Redirect URI Heading, Select Web and paste the CallbackURL that you copied from the Firebase Console Dialog Earlier.
- After about a Minute, Your App's Dashboard will be visible Copy the 'Application (client) ID' and Save it somewhere, this will be needed later.
  
#### C) Generate a new Azure Client Secret
- In the Same Page, Under the 'Manage' heading, click on 'Certificates and Secrets' and in the page that opens, Click on 'New Client Secret'
- Fill In the Details and once created, copy the String under the 'Value' Heading and save it somewhere, this is your Client Secret.
  
#### D) Complete the Firebase AuthProvider Setup
- Now go back to the Microsoft AuthProvider Dialog and paste the Application (client) ID and the Client Secret in the required fields and Click on Save!
- The Setup is Done! Now you can use Microsoft Authentication!
  
---
</details> 

<details><summary>🟢 Facebook</summary>

#### A) Create a Facebook App using the [Facebook Developer Page](https://developers.facebook.com)
  - Create a Facebook Developer Account or convert your existing account into a Developer Account
  - Click on Create App, Select Continue and Click Continue, fill in the necessary details and proceed
  - In the Dashboard, Click on 'Set Up' under the Facebook Login Section and click on Android
  - Now, Keep Clicking Next until instructed otherwise
  - Under 'Tell Us about Your Android Project', 
    - Add your Android Project's package name (see from AndroidManifest.xml)
    - Add **<your_package_name>.MainActivity** for DefaultActivityClassName and click 'Save'. In the dialog that pops up, Click 'Use this package name'
  - Keep Clicking Next until you arrive at the KeyHashes Section
  
#### B) Getting Your Development KeyHashes
  - **Windows Command**
    - Make Sure you have KeyTool from JDK(Java Development Kit)
    - [Download OpenSSL](https://code.google.com/archive/p/openssl-for-windows/downloads)
    - Execute this code in the Command Line (Note: The KeyStore Password is your Current PC User's password`): ```keytool -exportcert -alias androiddebugkey -keystore "C:\Users\<YOUR_USERNAME>\.android\debug.keystore" | " <YOUR_PATH_TO_OPENSSL_LIBRARY>\bin\openssl" sha1 -binary | "<YOUR_PATH_TO_OPENSSL_LIBRARY>\bin\openssl" base64```
  
  - **MacOS or Linux Command**
    - Execute this code in the Command Line: ```keytool -exportcert -alias androiddebugkey -keystore ~/.android/debug.keystore | openssl sha1 -binary | openssl base64```
  - Now Save the output, This will be needeed later
  - **Universal: To Get ReleaseKey (Optional For Now)**
    - Execute this code in the Command Line: ```keytool -exportcert -alias <YOUR_RELEASE_KEY_ALIAS> -keystore <YOUR_RELEASE_KEY_PATH> | openssl sha1 -binary | openssl base64```
  - Now Paste the Copied Keys to the Key Hashes Field and click on Save
  - Continue Clicking Next until Instructed Otherwise
  
#### C) Retrieve Your FacebookAppID
  - Under 'Edit Your Resources and Manifest', copy the value of facebook_app_id and save it somewhere, this will be needed later.
  - Do not Edit anything, Just Continue, The Manual Editing Work will be handled by FireSetup automatically
  - Keep Clicking Next and once you have reached the end, Close the Page!
  
#### D) Retrieve Your AppID and AppSecret from Facebook Login Settings
  - From the Dashboard, Go to the FB App Settings
  - Copy the AppID and AppSecret and save it somewhere, this is needed later 
 
#### E) Enable the Facebook SignIn Provider on the Firebase Console
  - Enable Facebook Authentication
  - Paste the AppID & App Secret in the respective fields
  - Copy the callbackURL (or) redirectURL and save it somewhere & Click on Continue
 
#### F) Register the RedirectURL in the Facebook Login Settings
  - Go to your FB Login Settings and paste the callbackURL in Valid OAuth Redirect URLs
  
#### G) Run FireSetup in FacebookSetup Mode
  - Open your Flutter Project in the Terminal
  - Run FireSetup in FacebookSetup Mode using this command: ```firesetup facebook -fbid=YOUR_FB_APP_ID```
  - This should Complete the Facebook Setup!
  
> Note: 🔴  You Need to Setup Facebook for iOS on your own! FireSetup cannot do it for you.
  
> Your Facebook Login App is currently in Development Mode, which means you can only login with the Account used for your Developer Account, To enable Everyone to Login, you need to Switch to Live Mode. Look it up Online.
  
</details>
  
---
  
### 🔵 Updating FireSetup
  After v0.4.0, FireSetup comes bundled with an UpdateEngine. It will let you know if a new update is available at anytime! It usually checks this before running your firesetup command!
  
  - Make Sure you have git installed (Should be done if you were able to install firesetup)
  - Run this command: ```firesetup update```
  - Done! Your FireSetup should now be upgraded to the latest stable version
    
---
