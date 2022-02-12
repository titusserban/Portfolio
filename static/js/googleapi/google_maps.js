// Load the map when the window loads
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initializeMap)
})


const initializeMap = () => {
    // Initialize the Google Maps Directions Service
    let directionsService = new google.maps.DirectionsService;
    // Initialize the Google Maps Directions Renderer
    let directionsDisplay = new google.maps.DirectionsRenderer;
    // Create the map object
    let map = new google.maps.Map(document.getElementById('map-route'), {
        zoom: 7,
        center: {lat: lat_a, lng: long_a}
    });
    // Render the map and the directions
    directionsDisplay.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsDisplay);

}

// Waypoints
const waypts = [
        {location: {lat: lat_c, lng: long_c},
        stopover: true},
        {location: {lat: lat_d, lng: long_d},
        stopover: true}
        ];

// Calculate and display the route
const calculateAndDisplayRoute = (directionsService, directionsDisplay) => {
    directionsService.route({
        origin: origin,
        destination: destination,
        waypoints: waypts,
        optimizeWaypoints: true,
        travelMode: google.maps.TravelMode.DRIVING,
    }, function(response, status) {
      // check if the response status is OK
      if (status === 'OK') {
        directionsDisplay.setDirections(response);
      } else {
        alert('Directions request failed due to ' + status);
        window.location.assign("/route")
      }
    });
}

// Show/hide directions
const DirectionsToggle = () => {
  const el = $('#dir-toggle');
  const dir_table = $('#dir-table')
  if (dir_table.attr("hidden") == "hidden") {
    dir_table.fadeIn()
    dir_table.removeAttr("hidden")
    el.html('hide <a href="javascript:void(0)" onclick="DirectionsToggle()">HERE')
  } else {
    dir_table.fadeOut()
    dir_table.attr("hidden", "hidden")
    el.html('click <a href="javascript:void(0)" onclick="DirectionsToggle()">HERE')
  }
}