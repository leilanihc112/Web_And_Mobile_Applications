# Team6-Spring2022

NOTE: This will not run locally. API keys, private keys, etc. that are necessary to run locally have been removed from the repository.

This is a crowd-sourcing application in which users can report whether an item at a merch stand at an event is
available or not. This is intended to help fans know whether it is worth it to stand in long merch lines at an
event or if the item is not even available anymore. This, in theory, will help make merch lines shorter and
save time for all fans at an event that want to purchase merchandise.

A MongoDB instance is used to store information and the web application is hosted on Google Cloud.

The users cannot access the website without having logged in first. If they attempt to reach any valid
URL and they are not currently logged in, they will be redirected to the login page.

After logging in, they are added to the database if this is the first time they have logged in. There is
no sign-up method.

Users can perform the following actions:
* Create stands and then create items for each stand
* Create posts on stands to indicate whether an item at that stand is available or not
* View all stands on the website
* View all posts that contain a specific tag
* Subscribe to stands that they would like an easily-accessible link to
* View all posts they have made so far
* View a specific stand and all of the posts that have been made on that stand by other users


Users will include the following information:
* Username
* Email
* List of subscribed stands


Stands include the following information:
* Name
* Location (latitude/longitude coordinates)
* Closing and opening date and time
* Inventory list of items available for purchase at the stand (optional)
* User that created the stand
* Photo associated with the stand (optional)


Items include the following information:
* Name
* Flag indicating whether the item is available


Posts include the following information:
* User that created the post
* Stand that the post was created on
* Title
* Body text
* Photos (optional)
* Tags (act as hashtags, which can be used to filter posts that have the same tag) (optional)


Notes about the web application: 
* The files in the web-app/generate_html/ directory contain scripts that can be used to generate the HTML templates used throughout the application, but are NOT used at runtime.
* The web-app/test_populate_database.py file is a script that can be used to populate the database with test values or delete all current values.
* The web-app/generate_templates.cmd file can be used to generate all HTML layouts that are generated by the scripts in the web-app/generate_html/ directory.


After cloning this repository, to run the website locally:

**Python 3.8 or higher required**

1. cd to the directory of the cloned repo
2. cd to the web-app directory
3. Run the following command to install required dependencies:
   ```pip install -r requirements.txt```
4. Run the following command to run the web application:
   ```python main.py```
5. Go to localhost:8080 in your browser to view the application!


To run the Android application locally:

1. Open Android Studio
2. Go to File > Open...
3. Select the Merchable/frontend/android.kotlin.todo folder and click "open"
4. Go to Run > Run 'app' and the emulator should start up with the Merchable app

To run React Native application locally:
1. Follow instructions to get your environment set up: https://reactnative.dev/docs/environment-setup
   * Use React Native CLI Quickstart
   * Target OS: Android
2. Navigate to React/Merchable_React
3. Get Libraries: Run "npm install"
4. Launch App: (In Android Studio, if using a virtual device)
   1. Run "npx react-native start" in one command line
   2. In another command line, run "npx react-native run-android"

