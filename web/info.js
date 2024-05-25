import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-analytics.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";
import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-database.js";

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

    // get user by uid
    const userRef = ref(db, "users/" + uid);
    onValue(userRef, (snapshot) => {
        const userData = snapshot.val();
        console.log(userData.username);
        const userName = userData.username;
        document.getElementById('userName').textContent = userName;
    });
}

function updateUserParameter(user) {
    const uid = user.uid;
    const dbRefparameter = ref(db, "users/" + uid);
    const speedElement = document.querySelector(".speedometer");
    var Speed = document.getElementById('speedvalue');

    const rpmElement = document.querySelector(".gear");
    var Rpm = document.getElementById('rpmvalue');

    const fuelElement = document.querySelector(".fuel");
    var Fuel = document.getElementById('fuelvalue');

    const tempElement = document.querySelector(".temp");
    var Temp = document.getElementById('tempvalue');

    onValue(dbRefparameter, (snapshot) => {
        const userData = snapshot.val();

        console.log('Speed: ' + userData.speedometer);
        const userspeedometer = userData.speedometer;
        Speed.textContent = userspeedometer;
        setSpeedValue(speedElement, userspeedometer);
    });
    
    onValue(dbRefparameter, (snapshot) => {
        const userData = snapshot.val();
        console.log('Rpm: ' + userData.rpm);
        const userrpm = userData.rpm;
        Rpm.textContent = (userrpm / 1000).toFixed(1);
        setRpmValue(rpmElement, userrpm / 1000);
    });

    onValue(dbRefparameter, (snapshot) => {
        const userData = snapshot.val();
        console.log('Fuel:' + userData.fuel);
        const userfuel = userData.fuel;
        Fuel.innerHTML = userfuel;
        setFuelValue(fuelElement, userfuel);
    });

    onValue(dbRefparameter, (snapshot) => {
        const userData = snapshot.val();
        console.log('Temp: ' + userData.temp);
        const usertemp = userData.temp;
        Temp.textContent = usertemp;
        setTempValue(tempElement, usertemp);
    });
    
}

function setSpeedValue(speed, valuespeed) {
    if (valuespeed < 0 || valuespeed > 300) {
        return;
    }
    speed.querySelector(".speedometer--needle").style.transform = `rotate(${(valuespeed - 160)}deg)`;

    if (valuespeed >= 150 && valuespeed <= 300) {
        document.getElementsByClassName("text--speed")[0].style.color = "red";
        showWarningSpeedToast();
    } else {
        document.getElementsByClassName("text--speed")[0].style.color = "white";
    }
}

function setRpmValue(gear, valuerpm) {
    if (valuerpm > 8) {
        return;
    }
    if (valuerpm == 0 || valuerpm == 8) {
        gear.querySelector(".gear--needle").style.transform = `rotate(${(valuerpm - 4) * 32.5}deg)`;
    }
    else {
        gear.querySelector(".gear--needle").style.transform = `rotate(${(valuerpm - 4) * 37}deg)`;
    }
    document.getElementsByClassName("value-rpm")[0].innerText = valuerpm;
}

function setFuelValue(fuel, valuefuel) {
    if (valuefuel < 0 || valuefuel > 100) {
        return;
    }
    fuel.querySelector(".fuel .fuel--needle").style.transform = `rotate(${(valuefuel - 50)}deg)`;
    if (valuefuel >= 0 && valuefuel <= 20) {
        document.querySelector(".icon-signal .fa-solid").style.color = "red";
        showWaringFuelToast();
    }
    else {
        document.querySelector(".icon-signal .fa-solid").style.color = "white";
    }
}

function setTempValue(temp, valuetemp) {
    if (valuetemp < 40 || valuetemp > 120) {
        return;
    }
    else {
        temp.querySelector(".temp--needle").style.transform = `rotate(${(valuetemp - 80) * 1.225}deg)`;
        if (valuetemp >= 100 && valuetemp <= 120) {
            document.querySelector(".temp--fill .fi").style.color = "red";
            showWarningTempToast();
        }
        else {
            clearInterval(intervalId);
            document.querySelector(".temp--fill .fi").style.color = "white";
        }
    }

}
onAuthStateChanged(auth, (user) => {
    if (user) {
        updateUserProfile(user);
        updateUserParameter(user);
    } else {
        alert("Create Account & Sign in");
        window.location.href = "signin-up.html";
    }
});

function toast({
    title = '',
    message = '',
    type = 'info',
    duration = 3000
  }) {
    const main = document.getElementById('toast');
    if (main) {
      const toast = document.createElement('div');
  
      // Auto remove toast
      const autoRemoveId = setTimeout(function () {
        main.removeChild(toast);
      }, duration + 2000);
  
      //Remove toast when click
      toast.onclick = function (e) {
        if (e.target.closest('.toast__close')) {
          main.removeChild(toast);
          clearTimeout(autoRemoveId);
        }
      }
  
      const icons = {
        success: 'fa fa-check-circle',
        info: 'fa fa-info-circle',
        warning: 'fa fa-exclamation-circle',
        error: 'fa fa-exclamation-circle',
      };
      const icon = icons[type];
      const delay = (duration / 1000).toFixed(2);
  
      toast.classList.add('toast', `toast--${type}`);
      toast.style.animation = `animation: slideInleft ease 0.3s, fadeOut linear 1s ${delay}s forwards;`;
      toast.innerHTML = `
            <div class="toast__icon">
                <i class="${icon}" aria-hidden="true"></i>
            </div>
            <div class="toast__body">
                <h3 class="toast__title">${title}</h3>
                <p class="toast__msg">${message}</p>
            </div>
            <div class="toast__close">
                <i class="fa fa-times" aria-hidden="true"></i>
            </div>
        `;
      main.appendChild(toast);
  
  
    }
  }
  
  function showWarningTempToast() {
    toast({
      title: 'Warning!',
      message: 'Engine overheating',
      type: 'warning',
      duration: 3000
    });
  }
  
  function showWarningSpeedToast() {
    toast({
      title: 'Warning!',
      message: 'You drive too fast',
      type: 'warning',
      duration: 3000
    });
  }
  
  function showWaringFuelToast() {
    toast({
      title: 'Warning!',
      message: 'Gasoline is about to run out',
      type: 'warning',
      duration: 3000
    });
  }
