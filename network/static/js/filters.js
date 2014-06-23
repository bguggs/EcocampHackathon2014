var optionsFile = "hack.options.json";
var options = {};
/*
function setFilterInput(key, parentNode){

	var optionVals = "<option value=\"\"></option>";

	if (key !== "None"){
		for (var i=0; i < options[key].length; i++){
			var val = options[key][i];
			//Show those values which are not "multiples."
			if (val.indexOf("+") === -1 && val!=""){
				optionVals += "<option value=\""+val+"\">"+val+"</option>";
			}
		}
	} else {
		applyFilters();
	}

	d3.select(parentNode).select(".selectVal").html(optionVals);
}*/

/*function clearFilters(){
	var keys = ["Total:"];
	var keysHTML = "<option value=\"None\">None</option>";

	for (var i=0; i < keys.length; i++){
		var key = keys[i];
		keysHTML += "<option value=\""+key+"\">"+key+"</option>";
	}

	d3.selectAll(".selectKey")[0].forEach(
		function(i){
			if (i.value=="None" || i.value==""){
				d3.select(i).html(keysHTML);
			}
		})
}

d3.json(optionsFile, function(error1, optionJSON) {
	//Variable Setup.
	options = optionJSON;
	clearFilters();
});

function applyFilters()
{

	//Show the graph again.
	recolorGraph();

	d3.selectAll(".edge").filter(function(e) { 
		var query = true;
		var filters = d3.selectAll(".filterGroup")[0];
		//Iterate through the filters and accumulate the results.
		filters.forEach(function(i){
		  if (query){
			var key = d3.select(i).select(".selectKey").node().value;
			//var val = d3.select(i).select(".selectVal").node().value;
	
			//If the value is empty, just recolor the graph.
			if (key=="None"){
				if (filters.length===1){
					query = false;
				}
			} else if (val==""){
				query = false;
			} else {
				if (e.target[key].indexOf(val)===-1 ||
					e.source[key].indexOf(val)===-1){
					query = false;
				}
			}
		  }
		});

		return query;
	}).attr("stroke-width", 2)
          .attr("stroke","#f46d43");

	//And likewise, remove any nodes that aren't connected to it.
	d3.selectAll(".node").filter(function(n){
		var query = true;

		var filters = d3.selectAll(".filterGroup")[0];
		//Iterate through the filters and accumulate the results.
		filters.forEach(function(i){
		  if (query){
			var key = d3.select(i).select(".selectKey").node().value;
			//var val = d3.select(i).select(".selectVal").node().value;
	
			if (key=="None"){
				if (filters.length===1){
					query = false;
				}
			} else if (val==""){
				query = false
			} else if (n[key].indexOf(val)===-1){
				query = false;
			}
		  }
		});

		return query;

	}).classed("filterSelectedNode", true);

	d3.selectAll(".filterSelectedNode > circle")	
	  .transition()
	  .delay(100)
	  .attr("fill","#d73027");
}

function addFilterInput(){
	d3.selectAll(".addFilterGroup")
	  .html("-")
	  .on("click", function(){
		d3.select(this.parentNode).remove();		
		applyFilters();
		});

	var selectMenus = "<select class=\"selectKey\"></select>"+
		"<select class=\"selectVal\"></select>";

	d3.select(".heading").append("span")
	  .attr("class", "filterGroup")
	  .html(selectMenus);

	var newGroup = d3.select(".filterGroup:last-child")

	newGroup.append("div")
		.attr("class", "addFilterGroup")
		.on("click", addFilterInput)
		.html("+");
	
	newGroup.select(".selectKey").on("change", function() {
		var key = this.value;
		//setFilterInput(key, this.parentNode);
	});

	newGroup.select(".selectVal").on("change", function() {
		applyFilters();
	});

	clearFilters();
}

*/
function filterLinks(d) {
	//Only allow clicks on visible nodes.
	if (d3.select(this.parentNode).style("opacity")==0){
		return false;
	}

	showGraph();
	showResetButton();

	//Variable Setup
	var id = d.id;
	var IDsToKeep = {};
	IDsToKeep[id] = true; //In case this node is an island.

	//Remove any edges that are not connected to the clicked one.
	d3.selectAll(".edge").filter(function(e) { 
		query = (e.target.id == id ||
			e.source.id == id );

		if (query){
				IDsToKeep[e.target.id]=true;
				IDsToKeep[e.source.id]=true;
		}

		//Select the nodes that aren't connected to id.
		return !query;
	}).attr("opacity", 0);

	//And likewise, remove any nodes that aren't connected to it.
	d3.selectAll(".node").filter(function(n){
		return IDsToKeep[n.id]==undefined;
	})
	  .attr("opacity", 0)
	  .style("cursor", "default");
}

function filterPieces(d) {
	//Only allow clicks on visible nodes.
	if (d3.select(this.parentNode).style("opacity")==0){
		return false;
	}

	showGraph();
	showResetButton();

	//Variable Setup
	var piece = d.piece;
	var IDsToKeep = {};
	IDsToKeep[d.id] = true; //In case this node is an island.

	//Remove any edges that are not connected to the clicked one.
	d3.selectAll(".edge").filter(function(e) { 
		query = (e.target.piece == piece ||
			e.source.piece == piece );

		if (query){
				IDsToKeep[e.target.id]=true;
				IDsToKeep[e.source.id]=true;
		}

		//Select the nodes that aren't connected to id.
		return !query;
	}).attr("opacity", 0);

	//And likewise, remove any nodes that aren't connected to it.
	d3.selectAll(".node").filter(function(n){
		return IDsToKeep[n.id]==undefined;
	})
	  .attr("opacity", 0)
	  .style("cursor", "default");
};
