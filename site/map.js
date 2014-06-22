d3.json("data2.json", function(error, data) {
    console.log(error)
   
    var id_map = {}
    for (var i=0; i<data.length; i++) {
	id_map[data[i].GEOID10] = i;
    }

    var map = L.mapbox.map('map', 'hamhands.ij464p4n')
	.setView([39.95, -75.1667], 13);
    
    var usLayer = omnivore.topojson("philly.json")
	.on('click', handleClick)
	.on('ready', colorMap)
	.addTo(map);

    
    var color = d3.scale.linear()
	.domain([0,4])
	.range(["green","red"]);

    function handleClick(e) {
	var id = e.layer.feature.properties.GEOID10;
	var lookup = id_map[id];
	makeCharts(data[lookup])
    makeInfo(data[lookup])
    }

    function colorMap(e) {
	console.log(e);	
	var items = e.target._layers;
	var keys = []
	for (var key in items) keys.push(key);

	var leaflets = $(".leaflet-clickable");
	console.log(leaflets)
	var colored = []
	for (var i=0; i<keys.length; i++) {
	    var id = items[keys[i]].feature.properties.GEOID10;
	    var lookup = id_map[id];
	    var myData = data[lookup];
	    var score = myData["LI_AVG"];
	    var myColor = color(score);
	    colored.push(myColor);
	}

	leaflets.each(function(i, d) {
	    d.attributes.fill = colored[i];
	    d.attributes.stroke = colored[i];
	    console.log(d.attributes.fill);
	});
    }
});
