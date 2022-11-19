let latitude, longitude; 
function geoFindMe() {

    const status = document.querySelector('#status');
    const mapLink = document.querySelector('#map-link');
  
    mapLink.href = '';
    mapLink.textContent = '';
  
    function success(position) {
       latitude  = position.coords.latitude;
       longitude = position.coords.longitude;
  
      status.textContent = '';
      mapLink.href = `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;
      mapLink.textContent = `Latitude: ${latitude} °, Longitude: ${longitude} °`;
    }
  
    function error() {
      status.textContent = 'Unable to retrieve your location';
    }
  
    if (!navigator.geolocation) {
      status.textContent = 'Geolocation is not supported by your browser';
    } else {
      status.textContent = 'Locating…';
      navigator.geolocation.getCurrentPosition(success, error);
    }
  
  }
//  console.log(latitude + " " + longitude + "dick");
  geoFindMe();
  console.log(latitude);
  setInterval(function() { geoFindMe(); }, 1000*10); // update every 30 s
 // document.querySelector('#find-me').addEventListener('click', geoFindMe);
//  var map, searchManager;

//     function GetMap() {
//         map = new Microsoft.Maps.Map('#myMap', {
//             credentials: 'Your Bing Maps Key',
//             center: new Microsoft.Maps.Location(47.678, -122.133),
//             zoom: 11
//         });

//         //Make a request to reverse geocode the center of the map.
//         reverseGeocode();
//     }

//     function reverseGeocode() {
//         //If search manager is not defined, load the search module.
//         if (!searchManager) {
//             //Create an instance of the search manager and call the reverseGeocode function again.
//             Microsoft.Maps.loadModule('Microsoft.Maps.Search', function () {
//                 searchManager = new Microsoft.Maps.Search.SearchManager(map);
//                 reverseGeocode();
//             });
//         } else {
//             var searchRequest = {
//                 location: map.getCenter(),
//                 callback: function (r) {
//                     //Tell the user the name of the result.
//                     alert(r.name);
//                 },
//                 errorCallback: function (e) {
//                     //If there is an error, alert the user about it.
//                     alert("Unable to reverse geocode location.");
//                 }
//             };

//             //Make the reverse geocode request.
//             searchManager.reverseGeocode(searchRequest);
//         }
//     } 