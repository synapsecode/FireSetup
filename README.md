<img src="https://i.ibb.co/9b9sbQS/New-Project.png" align="right">


# Flutter FireSetup Utility (0.2.0)
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
  ```
  Use the Firebase Console to do this! It's very straightforward
  ```
  
 ---
 
### 🟡 Step 3: Add an Android App in Firebase Console
  ```
  ○ Register the App
  ○ Save the google_services.json file in android/app
  ○ Click Next and do not proceed with editing any other files as This will be done by FireSetup
  ```

---

### 🟡 Step 4: Add Web App in Firebase Console
  ```
  ○ Register the App
  ○ From the code snippet provided by firebase, just copy the firebaseConfig object and save it somewhere
  ○ Click Next and do not proceed with editing any other files as This will be done by FireSetup
  ```
 
---

### 🟡 Step 5: Run FireSetup
  * Inside your flutter project, open cmd and enter this command (assuming you have installed FireSetup Correctly):

  ```batch
  firesetup -gcid="<YOUR_GOOGLE_SIGNIN_CLIENTID>" -efa="True"
  ```
  
  * The **-gcid** flag is useful for GoogleSignIn on the Web **(optional)**
  * The **-efa** flag stands for Enable FireAuth and if true, it adds the [FireAuth](https://github.com/synapsecode/fireauth) package to pubspec.yaml and replaces your main.dart file with an example snippet of how to use FireAuth **(optional)**

### 🟡 Step 5.1: Add firebaseConfig to Web
  ```
  ○ Open the flutter project using an IDE like VSCode for example
  ○ Go to the /web/index.html file and replace the firebaseConfig object there with the one you copied when adding the webApp
  ```
---

### 🟡 Step 6: Enable Authentication Methods
- Head over to the Authentication Section of your Firebase Project's Console
- Click on Get Started
- Go to the SignIn Method Tab
- Enable whichever Auth Provider you need!
---

### 🔵 Testing
  * Firstly, Get all the newly added packages
  * Write Some Code

    ```
    flutter pub get
    ```
  * Run the Application

    ```
    flutter run -d chrome (For Flutter Web)
    flutter run -d <device_identifier> (For Flutter Native)
    ```
---

Now, the basic setup is complete! You can use AnonymousSignIn and Mail SignIn directly provided you have enabled them in the Firebase Console.
To use Google SignIn, Phone SignIn and others, you need a bit more setup
After Enabling the respective authentication methods, follow these steps!

---

### 🟢 GoogleSignIn Additional Setup
  #### A) Get the GoogleSignInClientID (For FlutterWeb only)
  * Go to the [Google Cloud Platform Console](https://console.cloud.google.com)
  * Login With the Same Google Account used for Firebase
  * Open the GCP Project with the same name as your firebase project
  * Search Credentials in the Search Box and click on API Credentials
  * Copy the webClientID under OAuth 2.0 Client IDs
  * Go to /web/index.html and replace the placeholder string GCLIENTID with the copied clientID!

  #### B) Add the SHA-1 and SHA-256 Keys to Firebase
  * Go to your /android folder in the flutter project, open terminal and type this:

  ```batch
   gradlew signingReport
  ```
  * now, copy the SHA1 and SHA-256 Keys and store it somewhere.
  * Go to your firebase android app's settings in the [Firebase Console](https://console.firebase.google.com/)
  * Scroll to the bottom to 'SHA certificate fingerprints'
  * Click On 'Add Fingerprint' and add both the Keys. Done!

---

### 🟢 PhoneSignIn Additional Setup
  #### A) Add the SHA-1 & SHA-256 Keys (process shown above)
  
  #### B) Remove Android ReCaptcha Verification
  * Open your GCP Project (similar way as previously done)
  * search for Android Device Verification
  * Enable the API and done!

--- 

### 🟢 Twitter OAuth Additional Setup

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

### 🟢 Github OAuth Additional Setup

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
