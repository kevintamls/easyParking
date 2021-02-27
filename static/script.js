// Function to load the initial html page
function indexLoad() {
  // Div elements to add into html page defined
  var wrapper1 = document.createElement("div");
  wrapper1.id = "wrapper1";
  wrapper1.className = "wrapper";
  wrapper1.style.position = "relative";

  var leftColumn = document.createElement("div");
  leftColumn.id = "leftColumn";
  leftColumn.className = "fullcolumn";

  var extras = document.createElement("div");
  extras.id = "extras";
  extras.style.position = "fixed";
  extras.style.bottom = "0";
  extras.style.width = "100%"

  var mapCanvas = document.createElement("div");
  mapCanvas.id = "map";
  mapCanvas.width = "800px";
  mapCanvas.height = "600px";

  // Appending div elements into document body
  wrapper1.append(leftColumn);
  leftColumn.append(mapCanvas, extras);
  document.body.appendChild(wrapper1);
}

// Executes when document has finished loading (JQuery)
$(document).ready(function () {
  // Map Creation
  var mapCreated = 0 // Variable to check whether map has been created for if/else statement in AJAX
  // Map Object Definition
  mapboxgl.accessToken = 'pk.eyJ1Ijoia2V2aW50YW1scyIsImEiOiJja2xtYjhrbTIwN2lhMnBvMzZzNnBsaGlrIn0.My-zIZ0u7uBFCamIm2qDzA';
  var map = new mapboxgl.Map({
  container: 'leftColumn',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [114.1, 22.3],
  zoom: 10
  });
  
  // Adding Geocoder to map, powers search function on map
  map.addControl(
    new MapboxGeocoder({
      accessToken: mapboxgl.accessToken,
      mapboxgl: mapboxgl
    })
  );
  
  // AJAX function definition, takes jsonified dictionary from Python backend,
  // executed every 5 seconds for demo purposes.
  function fresh_ajax() {
    $.ajax({
      type: "GET",
      url: "/_get_data/",
      success: function (resp) {
        var coordinateJson = JSON.parse(resp.coordinates) // Parses jsonification to JS Object
        if (mapCreated === 0) { // If condition where if initial map hasn't been created, load
                                // resources for map + adds data source
          mapCreated = 1
          map.on('load', function() {
            map.loadImage(
              'https://docs.mapbox.com/mapbox-gl-js/assets/custom_marker.png',
              function (error, image) {
                if (error) throw error;
                map.addImage('custom-marker', image, {sdf: true});
                map.addSource('points', {
                  'type': 'geojson',
                  'data': coordinateJson})

                map.addLayer({
                  'id': 'points',
                  'type': 'symbol',
                  'source': 'points',
                  'layout': {
                  'icon-image': 'custom-marker',
                  'icon-size': 0.4,
                  // get the title name from the source's "title" property
                  'text-field': ['get', 'title'],
                  'text-font': [
                  'Open Sans Semibold',
                  'Arial Unicode MS Bold'
                  ],
                  'text-offset': [0, 1.25],
                  'text-anchor': 'top'
                  },
                  'paint': {
                    //'icon-color': '#FF0000'
                    'icon-color': [
                      'match',
                      ['get', 'avail'],
                      '0', '#008000',
                      '1', '#FF0000',
                      // '2', '#FF0000',
                      '#FF0000'                      
                    ]}
                  });
                }
              )
            }
          )
        }
        else {
          map.getSource('points').setData(coordinateJson) // Reloads new data from backend jasonification
        }
      }
    })
  }
  fresh_ajax(); // Initial execution of ajax function for map/data creation
  // object to exsecute fresh_ajax every 5 seconds
  window.setInterval(function () {
    fresh_ajax();
  }, 5000);
});