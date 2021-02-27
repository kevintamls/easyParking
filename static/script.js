function indexLoad() {
  var wrapper1 = document.createElement("div");
  wrapper1.id = "wrapper1";
  wrapper1.className = "wrapper";
  wrapper1.style.position = "relative";

  var leftColumn = document.createElement("div");
  leftColumn.id = "leftColumn";
  leftColumn.className = "fullcolumn";

  var headDivSupply = document.createElement("div");
  headDivSupply.className = "headdiv";
  headDivSupply.id = "backButton";
  headDivSupply.style.position = "relative";
  headDivSupply.style.verticalAlign = "middle";

  var headDivTitle = document.createElement("headerSpecial")
  headDivTitle.innerHTML = "Supply Air Temperature";
  headDivTitle.style.left = "3px";
  headDivTitle.style.top = "3px";
  headDivTitle.style.position = "relative";

  var extras = document.createElement("div");
  extras.id = "extras";
  extras.style.position = "fixed";
  extras.style.bottom = "0";
  extras.style.width = "100%"

  var mapCanvas = document.createElement("div");
  mapCanvas.id = "map";
  mapCanvas.width = "400px";
  mapCanvas.height = "300px";
  /*mapCanvas.style.display = "inline-block";
  mapCanvas.style.borderWidth = "0";
  mapCanvas.style.position = "absolute";*/

  wrapper1.append(leftColumn);
  leftColumn.appendChild(headDivSupply);
  headDivSupply.append(headDivTitle, mapCanvas, extras);

  document.body.appendChild(wrapper1);
  //document.body.appendChild(mapCanvas);
}

$(document).ready(function () {
  function fresh_ajax() {
    $.ajax({
      type: "GET",
      url: "/_get_data/",
      success: function (resp) {
        var coordinateJson = JSON.parse(resp.coordinates)
        console.log(typeof(resp.coordinates))
        console.log(coordinateJson)
        mapboxgl.accessToken = 'pk.eyJ1Ijoia2V2aW50YW1scyIsImEiOiJja2xtYjhrbTIwN2lhMnBvMzZzNnBsaGlrIn0.My-zIZ0u7uBFCamIm2qDzA';
        var map = new mapboxgl.Map({
        container: 'leftColumn',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [114.1, 22.3],
        zoom: 9
        });
        map.on('load', function() {
          map.loadImage(
            'https://docs.mapbox.com/mapbox-gl-js/assets/custom_marker.png',
            function (error, image) {
            if (error) throw error;
            map.addImage('custom-marker', image);
            map.addSource('points', {
              'type': 'geojson',
              'data': {
                "type": "Feature",
                "geometry": {
                "type": "Point",
                "coordinates": [-77.0323, 38.9131]
                },
              "properties": {
                "title": "test",
                "market-symbol": "monument"
              }
            }})
            map.addLayer({
              'id': 'points',
              'type': 'symbol',
              'source': 'points',
              'layout': {
              'icon-image': 'custom-marker',
              // get the title name from the source's "title" property
              'text-field': ['get', 'title'],
              'text-font': [
              'Open Sans Semibold',
              'Arial Unicode MS Bold'
              ],
              'text-offset': [0, 1.25],
              'text-anchor': 'top'
              }
              });
            }
            
          )

        })
        }
      })
    }

  fresh_ajax();

  
  /*window.setInterval(function () {
    fresh_ajax();
  }, 5000);*/
});