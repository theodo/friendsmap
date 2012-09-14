var geocoder;
var map;
var markers = [];
var infoWindow = new google.maps.InfoWindow;

function initialize() {
    initializeMap();
    initializeListener();
}

function initializeMap() {
    var mapOptions = {
        center: new google.maps.LatLng(48.856614, 2.352222),
        zoom: 8,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
}

function initializeListener() {
    $('#load_friends').click(function() {
        var i, length;
        var initialButtonText = $(this).text();
        $(this).text('Loading');
        for(i=0; i < markers.length; i++){
            markers[i].setMap(null);
        }
        markers = [];

        $.getJSON(apiUrl, function(friends) {
            for (i=0, length = friends.length; i < length; i++) {
                if (null != friends[i].location) {
                    addMarker(friends[i].location.lat, friends[i].location.lng, friends[i].name);
                }
            }
        })
        .success(function() {
            $('#load_friends').text(initialButtonText);
        });

        return false;
    });
}

function addMarker(lat, lng, name) {
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat, lng),
        map: map,
        draggable: false,
        animation: google.maps.Animation.DROP,
        title: name
    });

    google.maps.event.addListener(marker, 'click', function() {
        var marker = this;
        infoWindow.setContent('<h3>' + marker.getTitle() + '</h3>');
        infoWindow.open(map, marker);
    });

    markers.push(marker);
}