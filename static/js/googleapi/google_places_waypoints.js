// Initialize the autocomplete function after the window is loaded
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initializeAutocomplete())
})

const id_fields = ['a', 'b', 'c', 'd']

// Autocomplete function
const initializeAutocomplete = () => {

  // Iterate all the input fields
  for (i = 0; i < id_fields.length; i++) {
    let field = id_fields[i]
    // Create a new autocomplete object for each input
    window['autocomplete_' + field] = new google.maps.places.Autocomplete(
      // Identify the field
      document.getElementById('id-google-address-' + field),
    {
       // Select only addresses type
       types: ['address'],
       // Restrict autocomplete only to a country ( RO in this case )
       componentRestrictions: {'country': [base_country.toLowerCase()]},
    }).addListener('place_changed', function() {
          // Assing the geocode coordinates
          onPlaceChanged(field)
      });
  }
}

// Assign the Geocode coordinates (lat and long) based on the user input (aided by autocomplete) 
const onPlaceChanged = (identifier) => {

    // Variable construction and initialization
    let auto = window['autocomplete_'+ identifier]
    let el_id = 'id-google-address-' + identifier
    let lat_id = 'id-lat-' + identifier
    let long_id = 'id-long-' + identifier

    // Create the geocoder object
    let geocoder = new google.maps.Geocoder()
    // Get the input values
    let address = document.getElementById(el_id).value

    // Get the geographic coordinates based on the user input
    geocoder.geocode( {'address': address}, function(results, status) {

        if (status == google.maps.GeocoderStatus.OK) {
            // Get the latitude and longitude coordinates
            let latitude = results[0].geometry.location.lat();
            let longitude = results[0].geometry.location.lng();

            // Assing the values to the elements
            $('#' + lat_id).val(latitude)
            $('#' + long_id).val(longitude) 

            // Calculate the route once the latitude and longitude coordinates are received
            CalculateRoute()
        } 
    }); 
}


// Route calculation if the form is valid 
const CalculateRoute = () => {

    // Get the coordinates after geocoding results
    if ( validateForm() == true) {
      const params = {
          lat_a: $('#id-lat-a').val(),
          long_a: $('#id-long-a').val(),
          lat_b: $('#id-lat-b').val(),
          long_b: $('#id-long-b').val(),
          lat_c: $('#id-lat-c').val(),
          long_c: $('#id-long-c').val(),
          lat_d: $('#id-lat-d').val(),
          long_d: $('#id-long-d').val(),
      };

      // Encode the URI by replacing each instance of certain characters by one, two, three, or four escape sequences,
      // representing the UTF-8 encoding of the character 
      // (will only be four escape sequences for characters composed of two "surrogate" characters).
      let esc = encodeURIComponent;

      // Construct the query
      let query = Object.keys(params)
          .map(k => esc(k) + '=' + esc(params[k]))
          .join('&');

      // Construct the url
      url = '/googleapi/map?' + query

      // Automatically redirect to map generator page
      window.location.assign(url)
    }

}

// Validate form if all fields have an input value
const validateForm = () => {
    let valid = true;
    $('.geo').each(function () {
        if ($(this).val() === '') {
            valid = false;
            return false;
        }
    });
    return valid
}