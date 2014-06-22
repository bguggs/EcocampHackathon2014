d3.json(adjacencyFile, function(error1, adjacency) {
	d3.csv(dataFile, function(error2, data) {
		var width = parseInt(d3.select("body").style("width"), 10);
		var height = parseInt(d3.select("body").style("height"), 10);

		//Add a unique integer ID for each row.
		for (var i=0; i<data.length; i++){
			data[i]["id"] = i;
		}
	
		var network = makeNetwork(adjacency, data);
		applyPageRank(network, adjacency);
	
		drawGraph(network, width, height);
	});
});

function makeNetwork(adjacency, data){
	var network = {"nodes": [], "edges": []};

	for (var i=0; i < adjacency.length; i++){
		//Variable Setup.
		var nodeID = i;
		var nodeEdges = adjacency[i];
	
		//Create a node for this row.
		network.nodes.push(data[i]);
	
		//Create the necessary edges for this friend.
		for (j=0; j < nodeEdges.length; j++) {
			var otherNodeID = nodeEdges[j];
			network.edges.push({
					"source": nodeID, 
					"target": otherNodeID
					});
		}
	}
	return network;
}

//Grab a color for the node.
function colorScale(scaledRank){
	var colorArray = [
		"#7fcdbb",
		"#41b6c4",
		"#1d91c0",
		"#225ea8",
		"#253494",
		"#081d58"
		];

	var colorIndex = Math.floor((colorArray.length-1)*scaledRank);

	return colorArray[colorIndex]

}

//Actually draw the Graph.
function drawGraph(network, width, height){
	var force = d3.layout.force()
		.linkDistance(linkDistance)
		.nodes(network.nodes)
		.links(network.edges)
		.gravity(graphGravity)
		.charge(graphCharge)
		.size([ width, height ]);

	var zoom = d3.behavior.zoom()
		.scaleExtent([1/10, 2])
		.on("zoom", zoomed);

	var drag = d3.behavior.drag()
		.origin(function(d) { return d; })
		.on("dragstart", dragstarted)
		.on("drag", dragged)
		.on("dragend", dragended);


	var svg = d3.select("#networkGraph")
		.append("svg")
		.attr("width", width)
		.attr("height", height)
		.call(zoom);

	var container = svg.append("g"); //Allows zooming/panning.


	//Needed for zooming and dragging (http://bl.ocks.org/mbostock/6123708).
	function zoomed() {
		container.attr("transform", 
		"translate(" + d3.event.translate +")scale("+ d3.event.scale + ")");
	}

	function dragstarted(d) {
		d3.event.sourceEvent.stopPropagation();
		d3.select(this).classed("dragging", true);
	}
	
	function dragged(d) {
		d3.select(this)
		  .attr("cx", d.x = d3.event.x)
		  .attr("cy", d.y = d3.event.y);
	}
	
	function dragended(d) {
		d3.select(this).classed("dragging", false);
	}



	//Load the graph completely before displaying it.
	force.start();
	for (var i = numGraphIterations ; i>0; i--) force.tick();
	force.stop();

	d3.select("#loadingWheel").remove();

	var edge = container.selectAll(".edge")
		.data(network.edges)
		.enter().append("line")
		.attr("class", "edge")
		.attr("x1", function(d) { return d.source.x })
		.attr("y1", function(d) { return d.source.y })
		.attr("x2", function(d) { return d.target.x })
		.attr("y2", function(d) { return d.target.y });
	
	var node = container.selectAll(".node")
		.data(network.nodes)
		.enter().append("g")
		.attr("class", "node");

	node.append("circle")
		.attr("class", "circleNode") 
		.attr("r", function(d) { 
			return maxRadius*d.value+minRadius; })
		.on("mouseover", function() {
			//Put the current "g" on the top of the canvas.
			var g = this.parentNode;
			this.parentNode.parentNode.appendChild(g);

			d3.select(g).select("circle").transition().duration(100)
			  .attr("r", function(d) { 
				return (maxRadius*d.value+minRadius)*hoverScale;
				 })
			  .attr("stroke-width", 2);

			//Add some text content.
			var textbox = d3.select(g).append("g")
				.attr("class", "tooltipContainer")

			textbox.append("rect")
			  .attr("class", "tooltipBackground")
			  .attr("x", -100)
			  .attr("y", -20*tooltips.length-15)
			  .attr("width", 400)
			  .attr("height", 20*tooltips.length+10)
			  
			for (var i=0; i < tooltips.length; i++){
				textbox.append("text")
				  .attr("dx", -80)
				  .attr("dy", (-20*tooltips.length)+20*i+5)
				  .attr("text-anchor", "left")
				  .attr("class", "tooltip")
		 		  .text(function(d) { 
					return prettifiedTooltip(tooltips,i, d) 
					});

			}

		})
		.on("mouseout", function() {
			d3.select(this).transition().duration(100)
			  .attr("r", function(d) { 
				return maxRadius*d.value+minRadius; })
			  .attr("stroke-width", 1);

			//Remove the text content that was created.
			d3.select(".tooltipContainer").remove();
		})
		.on("click", clickFilter); 

	showGraph();
	recolorGraph();
	
	//Make sure the "g" element contains all of its children.
	node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
	
}


function updateWindow(){
	var width = d3.select("body").style("width");
	d3.select("svg").attr("width", width);
	d3.select("svg > g").attr("width", width);
}

//Set up the preliminary window.
window.onresize = updateWindow;
addFilterInput();
