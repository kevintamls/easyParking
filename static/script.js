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

  mapboxgl.accessToken = 'pk.eyJ1Ijoia2V2aW50YW1scyIsImEiOiJja2xtYjhrbTIwN2lhMnBvMzZzNnBsaGlrIn0.My-zIZ0u7uBFCamIm2qDzA';
  var map = new mapboxgl.Map({
  container: 'leftColumn',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [-74.5, 40],
  zoom: 9
  });
}

/*$(document).ready(function () {
  function fresh_ajax(gaugeRack, gaugePUE, tempGauge) {
    $.ajax({
      type: "GET",
      url: "/_get_data/",
      success: function (resp) {
        $('div#idcModelName1').text(resp.idcModelName1);
        $('div#idcModelName2').text(resp.idcModelName2);
        if (currentPage === 1 || currentPage === 2) {
          $('div#inttemp').text(resp.int);
          if (resp.idcModel === 2){
            $('div#inttemp2').text(resp.int2);
            $('div#rack1IntTemp').text(resp.rack1IntTemp);
            $('div#rack2IntTemp').text(resp.rack2IntTemp);
            $('div#rack1ExtTemp').text(resp.ext);
            $('div#rack2ExtTemp').text(resp.ext2);
          }
          $('div#exttemp').text(resp.ext);
          $('div#dispload').text(resp.load);
          $('div#realCoolCap').text(resp.realCoolCap);
          $('div#designLoadCap').text(resp.designLoadCap);
          $('div#avgPUE').text(resp.avgPUE);
          $('div#rack1Load').text(resp.rack1Load);
          $('div#rack2Load').text(resp.rack2Load);
          $('div#rack3Load').text(resp.rack3Load);
          $('div#kWindicator').text('(kW)');
          gaugeRack.value = resp.rawdata;
          gaugePUE.value = resp.avgPUE;
          tempGauge.value = resp.intGauge;
        }
        else if (currentPage === 3) {
          $('div#serialLabel').text(resp.serialLabel);
          $('div#rackConfigLabel').text(resp.rackConfigLabel);
          $('div#designCapInfoLabel').text(resp.designCapInfoLabel);
          $('div#controllerIPLabel').text(resp.controllerIPLabel);
          $('div#serial').text(resp.serial);
          $('div#rackConfig').text(resp.rackConfig);
          $('div#designCapInfo').text(resp.designCapInfo);
          $('div#controllerIP').text(resp.controllerIP);
          }
        }
      })
    }

  fresh_ajax(window.gaugeDisplay, window.gaugeDisplay2, window.tempGauge2);

  var mutationObserver = new MutationObserver(function() {
    fresh_ajax(window.gaugeDisplay, window.gaugeDisplay2, window.tempGauge2);
  });

  mutationObserver.observe(document.body, {childList: true});

  window.setInterval(function () {
    fresh_ajax(window.gaugeDisplay, window.gaugeDisplay2, window.tempGauge2);
  }, 5000);
});*/