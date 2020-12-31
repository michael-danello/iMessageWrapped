var getData = $.get('/data/contact_map')
getData.done(function(results) {
  var strResults = JSON.stringify(results);
  var data = results;
  buildContactsMap(data);
});


function buildContactsMap(data) {

  var mymap = L.map('mapid');

  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/{style}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: 'mdanello',
      style: 'ckj25cepg1h0t1ao84yleoi2z',
      tileSize: 512,
      zoomOffset: -1,
      accessToken: 'pk.eyJ1IjoibWRhbmVsbG8iLCJhIjoiY2tqMjBkYmZmMjkzMDJycnczOXNhcHVxNSJ9.744heLkvjePBkQ9LYUbElA'
  }).addTo(mymap);


    var arrayOfLatLngs = [];
    var zipcode;
    var maxPeople = 1;

    for (var zipcode in data) {
      if (data[zipcode]['people'].length > maxPeople) {
        maxPeople = data[zipcode]['people'].length
      };
    }

    var maxCircleWidth = 75;
    var peopleWidth = maxCircleWidth/maxPeople

    for (zipcode in data) {


    var place = data[zipcode]['place'];
    var people_formatted = data[zipcode]['people'].join("<br>")
    arrayOfLatLngs.push(place);


    var circle = L.circleMarker(place, {
        color: 'blue',
        fillColor: '#abb5d6',
        fillOpacity: .75-data[zipcode]['people'].length*.005,
        radius: data[zipcode]['people'].length * peopleWidth
    }).addTo(mymap);

    circle.bindPopup(people_formatted, {
      maxHeight: 100
    });

  };
  var bounds = new L.LatLngBounds(arrayOfLatLngs);
  mymap.fitBounds(bounds);
}
