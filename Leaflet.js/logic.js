function getColor(d) {
    return d > 5 ? '#840000':
           d > 4 ? '#c65102':
           d > 3 ? '#cb7723':
           d > 2 ? '#fdaa48':
           d > 1 ? '#ffff14':
           d > 0 ? '#89fe05':
                   '#FFEDA0';
}

// Store our API endpoint inside Url variables
var queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";
var tectonicUrl = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_plates.json";

d3.json(queryUrl, function(data) {
    d3.json(tectonicUrl, function(response) {
      createFeatures(data.features,response.features);
  });
});

function createFeatures(earthquakeData,platedata) {
    function onEachFeature(feature, layer) {
        layer.bindPopup("<h3>" + feature.properties.place + "</h3> <hr> <h4>Magnitude: " + feature.properties.mag + "</h4><p>When: " + new Date(feature.properties.time) +"</p>");
      }
 
    var earthquakes = L.geoJSON(earthquakeData, {
      onEachFeature: onEachFeature,
      pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, {
            radius: feature.properties.mag*5,
            fillColor: getColor(feature.properties.mag),
            color: "black",
            weight: 0.5,
            opacity: 0.8,
            fillOpacity: 0.8
        });
      }
    });

    var myStyle = {
      "color": "orange",
      "weight": 2,
      "opacity": 0.65,
      fillColor: "None"
    };
  
    var plates = L.geoJSON(platedata, {
      style: myStyle
    });

    // Sending our earthquakes layer to the createMap function
    createMap(earthquakes,plates);
  }

  function createMap(earthquakes,plates) {

    // Define base map layers
    var grayscaleMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.high-contrast",
      accessToken: API_KEY
    });

    var satelliteMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.streets-satellite",
      accessToken: API_KEY
    });

    var outdoorsMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.outdoors",
      accessToken: API_KEY
    });

    // Define a baseMaps object to hold our base layers
    var baseMaps = {
      "Satellite": satelliteMap,
      "Grayscale": grayscaleMap,
      "Outdoors": outdoorsMap
    };
  
    // Create overlay object to hold our overlay layer
    var overlayMaps = {
      Earthquakes: earthquakes,
      "Fault Lines": plates
    };
  
    // Create our map, giving it the satellitemap, earthquakes and plates layers to display on load
    var myMap = L.map("map", {
      center: [37.09, -95.71],
      zoom: 4,
      layers: [satelliteMap,plates,earthquakes]
    });
  
    // Create a layer control
    // Pass in our baseMaps and overlayMaps
    // Add the layer control to the map
    L.control.layers(baseMaps ,overlayMaps, {
      collapsed: false
    }).addTo(myMap);

    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (Map) {
  
      var div = L.DomUtil.create('div', 'info legend'),
          magnitudes = [0, 1, 2, 3, 4, 5],
          labels = [];
  
      // loop through our density intervals and generate a label with a colored square for each interval
      for (var i = 0; i < magnitudes.length; i++) {
          div.innerHTML +=
              '<i style="background:' + getColor(magnitudes[i] + 1) + '"></i> ' +
              magnitudes[i] + (magnitudes[i + 1] ? '&ndash;' + magnitudes[i + 1] + '<br>' : '+');
      }
  
      return div;
    };
    legend.addTo(myMap);
  }