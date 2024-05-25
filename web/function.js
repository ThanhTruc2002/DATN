var firebaseConfig = {
  apiKey: "AIzaSyAG8YqWXCErlZSLKUNR54NZ_NK7BTZU--g",
  authDomain: "mymap-e291c.firebaseapp.com",
  projectId: "mymap-e291c",
  storageBucket: "mymap-e291c.appspot.com",
  messagingSenderId: "663285944055",
  appId: "1:663285944055:web:6fa094eec315491756cdf2",
  measurementId: "G-T65LCW23PJ"
};
firebase.initializeApp(firebaseConfig);

var map = null;

function initializeMap(center, zoom) {
  if (map === null) {
    map = new google.maps.Map(document.getElementById('map'), {
      zoom: zoom,
      center: center
    });
  }
}

function processIRIData(data) {
  for (var key in data) {
    if (data.hasOwnProperty(key)) {
      var latitude = parseFloat(data[key].GPS.latitude);
      var longitude = parseFloat(data[key].GPS.longitude);
      var velocity = parseFloat(data[key].Velocity);
      var IRI = parseFloat(data[key].IRI);
      var color = get_color(velocity, IRI);

      addCircle(map, latitude, longitude, color);
    }
  }
}

function processPotholeData(data) {
  for (var key in data) {
    if (data.hasOwnProperty(key)) {
      var lat_pothole = parseFloat(data[key].GPS.latitude);
      var lng_pothole = parseFloat(data[key].GPS.longitude);

      addCircle(map, lat_pothole, lng_pothole, "black");
    }
  }
}

function processFirebaseData(snapshot, processData) {
  var data = snapshot.val();

  if (map === null) {
    var firstKey = Object.keys(data)[0];
    var firstLatitude = parseFloat(data[firstKey].GPS.latitude);
    var firstLongitude = parseFloat(data[firstKey].GPS.longitude);
    initializeMap({ lat: firstLatitude, lng: firstLongitude }, 18);
  }

  processData(data);
}

firebase.database().ref("/map/Pothole").on("value", function (snapshot) {
  processFirebaseData(snapshot, processPotholeData);
});

firebase.database().ref("/map/IRI").on("value", function (snapshot) {
  processFirebaseData(snapshot, processIRIData);
});

var thresholds = [
  [5, [[17.99, "yellowgreen"], [32.32, "yellow"], [Infinity, "red"]]],
  [10, [[8.99, "yellowgreen"], [16.16, "yellow"], [Infinity, "red"]]],
  [20, [[5.99, "yellowgreen"], [10.8, "yellow"], [Infinity, "red"]]],
  [30, [[4.49, "yellowgreen"], [8.08, "yellow"], [Infinity, "red"]]],
  [40, [[3.59, "yellowgreen"], [6.25, "yellow"], [Infinity, "red"]]]
];

function get_color(v, I) {
  for (var i = 0; i < thresholds.length; i++) {
    var v_min = thresholds[i][0];
    var thresholds_v = thresholds[i][1];
    if (v < v_min) {
      for (var j = 0; j < thresholds_v.length; j++) {
        var I_min = thresholds_v[j][0];
        var color = thresholds_v[j][1];
        if (I < I_min) {
          return color;
        }
      }
    }
  }
  return "yellowgreen";
}

function addCircle(map, latitude, longitude, color) {
  var circle = new google.maps.Circle({
    strokeColor: color,
    strokeOpacity: 1,
    strokeWeight: 1,
    fillColor: color,
    fillOpacity: 0.8,
    center: { lat: latitude, lng: longitude },
    radius: 1 // Điều chỉnh bán kính của chấm nhỏ tại đây
  });

  circle.setMap(map);

  var infoWindow = new google.maps.InfoWindow({
    content: "Latitude: " + latitude + "<br>Longitude: " + longitude
  });

  circle.addListener('click', function () {
    infoWindow.setPosition(circle.getCenter());
    infoWindow.open(map);
  });
}


//////////////////////////////////////////////////////////////////////////////////////////////

// Toast function
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