/* Some Code taken from
http://bl.ocks.org/mbostock/3887235
*/

function makeCharts(data) {
    
    $("#charts").empty();
    // Get all of the keys in the data
    var keys = [];
    for (var k in data) keys.push(k);

    // ######### Making the pie chart ################
    var pie_data = []
    for (var i=0; i<keys.length; i++) {
	if (keys[i].length > 10) {
	    if (!(keys[i].slice(0,5) == "Speak") && !(keys[i].slice(0,1) == "$")) {
		pie_data.push({"value":+data[keys[i]],"name":keys[i]});
	    }
	}
	else {
	    if (!(keys[i].slice(6) == "_AVG") && !(keys[i] == "id") && !(keys[i] == "GEOID10") && !(keys[i] == "Less than $10,000") && !(keys[i] == "RB_CUSTMR")) {
		pie_data.push({"value":+data[keys[i]],"name":keys[i]});
	    }
	}
    }

    console.log(pie_data)
    var width = 300,
	height = 200,
    radius = Math.min(width, height) / 2;

    var color = d3.scale.ordinal()
	.range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

    var arc = d3.svg.arc()
	.outerRadius(radius - 10)
	.innerRadius(0);

    var pie = d3.layout.pie()
	.sort(null)
	.value(function(d) { return d.value; });

    var svg = d3.select("#charts").append("svg")
	.attr("width", width)
	.attr("height", height)
	.append("g")
	.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var g = svg.selectAll(".arc")
	.data(pie(pie_data))
	.enter().append("g")
	.attr("class", "arc");

    g.append("path")
	.attr("d", arc)
	.style("fill", function(d) { 
	    console.log(d.data.name)
	    return color(d.data.name); });

    g.append("text")
	.attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
	.attr("dy", ".35em")
	.style("text-anchor", "middle")
	.text(function(d) { return d.data.name; });
}
