function updateRequestButton(rideType) {
  var requestButton = document.getElementById('request-ride');
  requestButton.textContent = 'Request ' + rideType;
}

document.addEventListener('DOMContentLoaded', function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;
            console.log("Latitude: " + latitude + ", Longitude: " + longitude);
        }, function() {
            console.log("Geolocation is supported, but it failed");
        });
    } else {
        console.log("Geolocation is not supported by this browser.");
    }

    var rideOptions = document.querySelectorAll('.ride-option');
    rideOptions.forEach(function(option) {
        option.addEventListener('click', function() {
            showRideDetails(this);
        });
    });
});

function updateRequestButton(rideType) {
    var requestButton = document.getElementById('request-ride');
    requestButton.textContent = 'Request ' + rideType;
}

function showRideDetails(rideOption) {
    var rideName = rideOption.querySelector('h3').textContent;
    var rideDescription = rideOption.querySelector('p').textContent;
    var ridePrice = rideOption.querySelector('.price').textContent;

    // Display details in a designated area or as an alert (for simplicity)
    alert("Ride Details:\n" + rideName + "\n" + rideDescription + "\nPrice: " + ridePrice);
}
