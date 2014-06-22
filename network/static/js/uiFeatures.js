function prettifiedTooltip(tooltips, i, d){
	var title = tooltips[i][1] + ": ";
	var rawText = d[tooltips[i][0]];
	var prettyText = rawText.split("+").join(", ");

	return title + prettyText;
}


function recolorGraph(){
	//Clear the previous filters.
	d3.selectAll(".filterSelectedNode").classed("filterSelectedNode", false);	
	d3.selectAll(".edge")
		.attr("stroke-width", 1)
		.attr("stroke", "#acacac");
	d3.selectAll("circle").transition().delay(50)
		.attr("stroke", "black")
		.attr("stroke-width", 1)
		.attr("fill", function(d) { return colorScale(d.value) });
}

function showGraph(){
	d3.selectAll(".edge")
		.attr("opacity", 1);
	d3.selectAll(".node")
		.style("cursor", "pointer")
		.attr("opacity", 1);
	d3.selectAll("#resetButton").remove();
}

function showResetButton(){
	d3.selectAll("#resetButton").remove();
	d3.select(".heading").append("div")
		.attr("id", "resetButton")
		.attr("onclick","showGraph();")
		.html("Show All");
	
}

