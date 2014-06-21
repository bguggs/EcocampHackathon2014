d3.json("RecycleBank_Customers.geojson", function(error, data) {
    console.log(error)


    var partial_latlngs = [];
    for (var i=0; i<1000; i++) {
	var lng = parseFloat(data.features[i].geometry.coordinates[0]);
	var lat = parseFloat(data.features[i].geometry.coordinates[1]);
	partial_latlngs.push([lat,lng]);
    }

    console.log("data: ", partial_latlngs)

    var map = L.mapbox.map('map', 'examples.map-i86nkdio')
	.setView([39.95, -75.1667], 13);

    var geojsonMarkerOptions = {
	radius:3,
	fillColor: "#fff",
	color: "#000",
	weight: 1,
	opacity: 1,
	fillOpacity: 0.8,
	title: "test"
    };
													    
    for (var j=0; j<partial_latlngs.length; j++) {
	var circle = L.circleMarker(partial_latlngs[j],geojsonMarkerOptions)
	circle.addTo(map);
    }

    var polygon = L.polygon(partial_latlngs.slice(0,4));
    polygon.addTo(map);
});
