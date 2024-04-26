import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-analytics.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";
import { getDatabase, ref, get } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-database.js";

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
const db = getDatabase();
const auth = getAuth();
const user = auth.currentUser;

function updateUserProfile(user) {
    const uid = user.uid;
    
    const usernameRef = ref(db, `users/${uid}/username`);
    console.log(uid)
    console.log(usernameRef)

    // Lắng nghe sự thay đổi trong node tên người dùng
    // onValue(usernameRef, (snapshot) => {
    //     const username = snapshot.val(); // Lấy giá trị tên người dùng từ snapshot
    //     if (username) {
    //         document.getElementById('userName').textContent = username;
    //     }
    // });
    // const userName = user.displayName;
    // const userEmail = user.email;
    // const userPhoto = user.photoURL;

    document.getElementById('userName').textContent = usernameRef;
}

onAuthStateChanged(auth, (user) => {
    if (user) {
        updateUserProfile(user);
    } else {
        alert("Create Account & Sign in");
        window.location.href = "sign_up.html";
    }
});