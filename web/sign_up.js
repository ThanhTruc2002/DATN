import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-database.js";

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
const db = getDatabase();

//signup button
const signup = document.getElementById('signup');
signup.addEventListener('click', function (event) {
    event.preventDefault()
    //inputs
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // User signed up successfully
            var user = userCredential.user;

            console.log("User signed up:", user);

            // var user_data = {
            //     email: email,
            //     username: username
            // };
            // //set user data to database
            // database_ref.child('/users' + username).set(user_data)
            alert("Sign Up...")
            window.location.href = "web_map.html";
            // ...
        })
        .catch((error) => {
            // An error occurred during sign up
            var errorCode = error.code;
            var errorMessage = error.message;
            console.error("Sign up error:", errorCode, errorMessage);
            alert(errorMessage)
        });
    onAuthStateChanged(auth, (user) => {
        console.log(user)
        const uid = user.uid;
        set(ref(db, 'users/' + uid), {
            email: email,
            username: username
        })
    })
})

