d3.json("data.json", function(error, data) {
    console.log(error)
   
    var id_map = {}
    for (var i=0; i<data.length; i++) {
	id_map[data[i].GEOID10] = i;
    }

    var map = L.mapbox.map('map', 'examples.map-i86nkdio')
	.setView([39.95, -75.1667], 13);
    
    var usLayer = omnivore.topojson("philly.json")
	.on('click', handleClick)
	.addTo(map);


    function handleClick(e) {
	var id = e.layer.feature.properties.GEOID10;
	var lookup = id_map[id];
	console.log(data[lookup]);
    }
});
