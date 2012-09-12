var geocoder;
var map;
function initialize() {

  var mapOptions = {
    center: new google.maps.LatLng(48.856614, 2.352222),
    zoom: 8,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
}