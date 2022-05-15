Make sure to install the following before running:
- npm install -g expo-cli
- npm install @react-navigation/native @react-navigation/native-stack
- expo install react-native-screens react-native-safe-area-context

Run from this directory:
- npm start

In another command line, run for the device of your choice. As an example, for Android: 
- npm run android

1. On the Home page, you can see your cat! Typing a name for the cat will change the text below the cat to say its name instead of "your cat"
2. You can press the button to feed the cat some milk. When you do, the text will change to say "I am full" instead of "I am hungry", and an alert will pop up saying "Thank You!" and the button will also be disabled and say the same.
3. A list of movies fetched from a request made to a specified URL is also displayed on the Home page.
4. There are three navigation buttons: 
- "View Some Images" will go to a view that contains images that can be scrolled through horizontally.
- "Drag a Square" will go to a view that allows you to drag and release a square, and it will always return to the center
- "View a List" will go to a section list of names 