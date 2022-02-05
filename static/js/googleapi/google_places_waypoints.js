$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initAutocomplete())

})

const auto_fields = ['a', 'b', 'c', 'd']

const initAutocomplete = () => {

  for (i = 0; i < auto_fields.length; i++) {
    let field = auto_fields[i]
    window['autocomplete_' + field] = new google.maps.places.Autocomplete(
      document.getElementById('id-google-address-' + field),
    {
       types: ['address'],
       componentRestrictions: {'country': [base_country.toLowerCase()]},
    })
  }

  autocomplete_a.addListener('place_changed', function(){
          onPlaceChanged('a')
      });
  autocomplete_b.addListener('place_changed', function(){
          onPlaceChanged('b')
      });
  autocomplete_c.addListener('place_changed', function(){
          onPlaceChanged('c')
      });
  autocomplete_d.addListener('place_changed', function(){
          onPlaceChanged('d')
      });
}


const onPlaceChanged = (addy) => {

    let auto = window['autocomplete_' + addy]
    let el_id = 'id-google-address-' + addy
    let lat_id = 'id-lat-' + addy
    let long_id = 'id-long-' + addy

    let geocoder = new google.maps.Geocoder()
    let address = document.getElementById(el_id).value

    geocoder.geocode( { 'address': address}, function(results, status) {

        if (status == google.maps.GeocoderStatus.OK) {
            let latitude = results[0].geometry.location.lat();
            let longitude = results[0].geometry.location.lng();

            $('#' + lat_id).val(latitude) 
            $('#' + long_id).val(longitude) 

            CalcRoute()
        } 
    }); 
}


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


const CalcRoute = () => {

    if ( validateForm() == true){
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

      let esc = encodeURIComponent;
      let query = Object.keys(params)
          .map(k => esc(k) + '=' + esc(params[k]))
          .join('&');

      url = '/googleapi/map?' + query
      window.location.assign(url)
    }

}