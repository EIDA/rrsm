var vectorSource = new ol.source.Vector({
    features: []
});

var vectorLayer = new ol.layer.Vector({
    source: vectorSource
});

var map = new ol.Map({
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()
        }), vectorLayer
    ],
    interactions: ol.interaction.defaults({mouseWheelZoom:false}),
    target: document.getElementById('map'),
    view: new ol.View({
        center: ol.proj.fromLonLat([5, 52]),
        zoom: 2
    })
});

var element = document.getElementById('popup');

var popup = new ol.Overlay({
    element: element,
    positioning: 'bottom-center',
    stopEvent: false,
    offset: [5, -30]
});
map.addOverlay(popup);

// display popup on click
map.on('click', function (evt) {
    var feature = map.forEachFeatureAtPixel(evt.pixel,
        function (feature) {
            return feature;
        });
    if (feature) {
        // Make sure the popup is disposed (when clicking new marker before
        // deselecting the previous one, popup was showing previous marker data.
        $(element).popover('dispose');
        var coordinates = feature.getGeometry().getCoordinates();
        popup.setPosition(coordinates);
        $(element).popover({
            'placement': 'top',
            'html': true,
            'content': feature.get('name')
        });
        $(element).popover('show');
    } else {
        $(element).popover('dispose');
    }
});

// change mouse cursor when over marker
map.on('pointermove', function (e) {
    if (e.dragging) {
        $(element).popover('dispose');
        return;
    }
    var pixel = map.getEventPixel(e.originalEvent);
    var hit = map.hasFeatureAtPixel(pixel);
    map.getTarget().style.cursor = hit ? 'pointer' : '';
});

var getEventColor = function (value) {
    if (value < 4.0) {
        return '#17A2B8' // Bootstrap info
    } else if (value < 6.0) {
        return '#FFC107' // Bootstrap warning
    } else {
        return '#DC3545' // Bootstrap danger
    }
}

var zoomReset = function () {
    $(element).popover('dispose');
    map.getView().animate({
        center: ol.proj.fromLonLat([5, 52]),
        duration: 1000,
        zoom: 2
    })
}

var focusEvent = function (lat, lon, zoom=8) {
    $(element).popover('dispose');
    map.getView().animate({
        center: ol.proj.fromLonLat([lon, lat]),
        duration: 1000,
        zoom: zoom
    })
}

var focusOnCountry = function(countryCode, zoom=6){
    let lat, lon = 0;

    switch (countryCode){
        case "es":
        lat = 40.463667;
        lon = -3.74922;
        break;
        case "it":
        lat = 41.87194;
        lon = 12.56738;
        break;
        case "gr":
        lat = 39.074208;
        lon = 21.824312;
        break;
        case "tr":
        lat = 38.963745;
        lon = 35.243322;
        break;
        case "ch":
        lat = 46.818188;
        lon = 8.227512;
        zoom = 7
        break;
    }

    focusEvent(lat, lon, zoom);
}