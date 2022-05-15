/**
 * Copyright 2018, Google LLC
 * Licensed under the Apache License, Version 2.0 (the `License`);
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an `AS IS` BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { auth } from './firebase.js';

window.addEventListener('load', function () {
	document.getElementById('sign-out').onclick = function () {
		if (window.confirm("Are you sure you want to sign out?")) {
			auth.signOut().then(function () {
				window.alert("You have been successfully signed out");
				window.location.href = "/logout";
			});
		}
	};
	
	document.body.style.background = '#252526';
	
	// FirebaseUI config.
	var uiConfig = {
	  signInSuccessUrl: '/',
	  signInOptions: [
		// Comment out any lines corresponding to providers you did not check in
		// the Firebase console.
		firebase.auth.GoogleAuthProvider.PROVIDER_ID,
		firebase.auth.EmailAuthProvider.PROVIDER_ID,
	  ],
	};

    auth.onAuthStateChanged(function (user) {
      if (user) {
        // User is signed in, so display the "sign out" button and login info.
        user.getIdToken().then(function (token) {
          // Add the token to the browser's cookies. The server will then be
          // able to verify the token against the API.
          // SECURITY NOTE: As cookies can easily be modified, only put the
          // token (which is verified server-side) in a cookie; do not add other
          // user information.
          document.cookie = "token=" + token;
        });
      } else {
		  // User is signed out.
		  // Initialize the FirebaseUI Widget using Firebase.
		  var ui = new firebaseui.auth.AuthUI(auth);
		  // Clear the token cookie.
		  document.cookie = "token=";
		  document.getElementById('sign-out').hidden = true;
		  // Show the Firebase login button.
		  ui.start('#firebaseui-auth-container', uiConfig);
	  }
    }, function (error) {
      console.log(error);
      alert('Unable to log in: ' + error)
    });
  });