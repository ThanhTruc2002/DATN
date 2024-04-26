import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-analytics.js";
import { getAuth, signInWithEmailAndPassword, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";

var firebaseConfig = {
    apiKey: "AIzaSyAG8YqWXCErlZSLKUNR54NZ_NK7BTZU--g",
    authDomain: "mymap-e291c.firebaseapp.com",
    projectId: "mymap-e291c",
    storageBucket: "mymap-e291c.appspot.com",
    messagingSenderId: "663285944055",
    appId: "1:663285944055:web:6fa094eec315491756cdf2",
    measurementId: "G-T65LCW23PJ"   
};
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth();
const user = auth.currentUser;

//signin button
const signin = document.getElementById('signin');
signin.addEventListener('click', function (event) {
    event.preventDefault()
    //inputs
    // const username = document.getElementById('username');
    const email = document.getElementById('email-signin').value;
    const password = document.getElementById('password-signin').value;

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // User signed up successfully
            var user = userCredential.user;
            console.log("User signed in:", user);
            // alert("Sign In...")
            window.location.href = "web_map.html";
            // ...
        })
        .catch((error) => {
            // An error occurred during sign up
            var errorCode = error.code;
            var errorMessage = error.message;
            alert(errorMessage)
        });
    
})
