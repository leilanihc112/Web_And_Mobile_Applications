import "https://www.gstatic.com/firebasejs/7.14.5/firebase-app.js";
import "https://www.gstatic.com/firebasejs/7.8.0/firebase-auth.js";

const config = {
	apiKey: "AIzaSyDvtpPao8ZTSkjZKysbaycyLgBovCn76fA",
	authDomain: "team6merchable.firebaseapp.com",
	projectId: "team6merchable",
	storageBucket: "team6merchable.appspot.com",
	messagingSenderId: "1012349947363",
	appId: "1:1012349947363:web:402c6208abee111204a4d6",
	measurementId: "G-N3Y2ZTW032"
};

if (!firebase.apps.length) {
	firebase.initializeApp(config);
}

export const auth = firebase.auth();