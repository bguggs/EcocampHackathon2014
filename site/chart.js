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
	    if (!(keys[i].slice(0,5) == "Speak") && !(keys[i].indexOf("$") > -1)) {
		pie_data.push({"value":+data[keys[i]],"name":keys[i]});
	    }
	}
	else {
	    if (!(keys[i].slice(6) == "_AVG") && !(keys[i] == "id") && !(keys[i] == "GEOID10") && !(keys[i].indexOf("$") > -1) && !(keys[i] == "RB_CUSTMR") && !(keys[i] == "Total:")) {
		pie_data.push({"value":+data[keys[i]],"name":keys[i], "population":data.Total:});
	    }
	}
    }
    
    $("#charts").append("<div id=\"langName\"><h3>Language: <span id=\"lang\"> </span></h3></div>");
    console.log(pie_data)
    var width = 300,
	height = 200,
    radius = Math.min(width, height) / 2;

    var color = d3.scale.ordinal()
	.range(['rgb(166,206,227)','rgb(31,120,180)','rgb(178,223,138)','rgb(51,160,44)','rgb(251,154,153)','rgb(227,26,28)','rgb(253,191,111)','rgb(255,127,0)','rgb(202,178,214)','rgb(106,61,154)','rgb(255,255,153)','rgb(177,89,40)']);

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
	.attr("title", function(d) { return d.data.name; })
	.style("fill", function(d) { 
	    return color(d.data.name); })
	.on('click', function(d) {
	    $("#charts #langName span").html(d.data.name.slice(0,-1).append(" -- Population: ").append(d.data.population);
	});

    $("#charts").append("<div id=\"description\">Languanges other than English spoken in the selected tract.</div>");
    
    // ############ Bar Chart Code ###################

}

function makeInfo(data){
  
	for (var k in data) keys.push(k);

	for (var i=0; i < keys.length; i++){
		if (keys[i] == "ApproxAvgIncome"){
			var AvgInc = keys[i];
			document.getElementById('Income').innerHTML = AvgInc;
		}

		if (keys[i] == "LI_AVG"){
			var LIAVG = keys[i];
			document.getElementById('LitterIndex').innerHTML = LIAVG;
		}

		if (keys[i] == "RB_CUSTMR){
			var RBCust = keys[i];
			document.getElementById('RecycleBank').innerHTML = RBCust;
		}
}



