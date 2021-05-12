# Flutter FireSetup Utility
A Simple Automated way of Adding Firebase to your flutter project! Makes the process easy as you do not need to individually go into each file and add code snippets! The script takes care of that for you!
As a bonus, you can integrate my [FireAuth](https://github.com/synapsecode/fireauth) package effortlessly by using this script.
It uses Python internally

## System Requirements
* Windows 10
* Python 3.7.1 and above

## Installation
* Make sure you have python installed, type python in cmd & if the python prompt opens, you can continue.
* Git Clone this Project into a folder of your choice
* Add the path (where the python source code exists) to your PATH environment variable
* Close all CMD instances and reopen and now you should be able to use firesetup from anywhere on your computer

### NOTE: 🔴🔴 Adds Firebase to Android and Web Only ❗ Add Firebase to iOS on your own

## Usage

### 👉 Step1: Create a flutter project
```batch
flutter create testapp
cd testapp
```

### 👉 Step2: Create a Firebase Project (or) Open an Existing One
  This is very straightforward

### 👉 Step3: Add an Android App in Firebase Console
   * Follow the Steps
   * Save the google_services.json file in android/app
   * Click Next and do not proceed with editing any other files

### 👉 Step4: Add Web App in Firebase Console
   * Follow the Steps
   * Copy the firebaseConfig object from the code provider by firebase and save it, you will need this later

### 👉 Step 5: Get your GoogleSignIn ClientID (Optional if you do not want GoogleSignIn)
  * Go to the [Google Cloud Platform Console](https://console.cloud.google.com)
  * Login With the Same Google Account used for Firebase
  * Open the GCP Project with the same name as your firebase project
  * Search Credentials in the Search Box and click on API Credentials
  * Copy the webClientID under OAuth 2.0 Client IDs

### 👉 Step 6: Using FireSetup
  * Inside your flutter project, open cmd and enter this command (assuming you have installed FireSetup Correctly):

  ```batch
  firesetup -gcid="GOOGLE_SIGNIN_CLIENTID" -efa="True"
  ```
  
  * The **-gcid** flag is useful for GoogleSignIn on the Web (optional)
  * The **-efa** flag stands for Enable FireAuth and if true, it adds the [FireAuth](https://github.com/synapsecode/fireauth) package to pubspec.yaml and replaces your main.dart file with an example snippet of how to use FireAuth (optional)

### 👉 Step 6.1:  Step Add firebaseConfig to Web
  * Open the flutter app using an IDE like VSCode for example
  * Go to the /web/index.html file and replace the firebaseConfig object there with the one you copied when adding the webApp

### 👉 Step 7: Add SHA-1 & SHA-256 Keys to Firebase Android App
  * Go to your /android folder in the flutter project, open terminal and type this:

  ```batch
   gradlew signingReport
  ```
  
  now, copy the SHA1 and SHA-256 Keys, store it for later use and add it to your Firebase Project
  
### 👉 Step 8: (If Enabled FireAuth) Enable Authentication Methods
  * Go to your Firebase Console > Authentication
  * Go to SignIn Methods
  * Enable all the Authentication methods you need, FireAuth supports (Google, Anonymous, Email&Password, Phone)

### 👉 Step 9: (If enabled FireAuth & Using PhoneAuth) Remove Android ReCaptcha Verification
  * Open your GCP Project (similar way as previously done)
  * search for Android Device Verification
  * Enable the API

### 👉 Step 10: Testing
  * Firstly, Get all the newly added packages

    ```
    flutter pub get
    ```
  * Run the Application

    ```
    flutter run -d chrome (For Flutter Web)
    flutter run -d <device_identifier> (For Flutter Native)
    ```
   
