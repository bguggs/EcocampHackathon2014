function PageRankFormula(n, weightedSum){
	//Let n === number of nodes total
	var d = 0.85; // "Damping Factor" -- commonly set to 85%.
	return (1-d)/n + d*weightedSum;
}

function applyPageRank(network, adjacencyDict){
	//Variable Setup.
	var nodes = network.nodes;
	var num_nodes = nodes.length;
	var outgoingEdges = adjacencyDict;
	var numIterations = 3;
	var oldWeights = {};
	var incomingEdges = Array.apply([], Array( nodes.length)).map(
					function () { return [] }
				); 

	//Find all the nodes that link to a specific node.
	for (var i=0; i < nodes.length; i++){
		var nodeID = nodes[i]["id"];
		var nodeEdges = outgoingEdges[nodeID];
		
		//Just to make sure each node is accounted for...
		if (incomingEdges[nodeID]===undefined){
			incomingEdges[nodeID] = [];
		}

		for (var j=0; j < nodeEdges.length ; j++){
			var otherNode = nodeEdges[j];
			
			if (incomingEdges[otherNode]===undefined){
				incomingEdges[otherNode] = [];
			}

			incomingEdges[otherNode].push(nodeID);
		}
	}
	



	//Initiate the weights as just the probability of choosing any random node.
	var initialProb = 1/parseFloat(nodes.length);
	for (var i=0; i < nodes.length; i++){
		var node = nodes[i];
		oldWeights[node["id"]] = initialProb;
	}
	

	for (var i=1; i<= numIterations; i++){
		//Variable Setup.
		var currentWeights = {};
		var rankMax = 0,
		    rankMin = 1;

		for (var j=0; j < nodes.length ; j++){
			//Varjable Setup.
			var node = nodes[j];
			var nodeIncoming = incomingEdges[node["id"]];
			var oldWeight = oldWeights[node["id"]];
			var sumOut = 0;
	
			for (var k=0; k < nodeIncoming.length ; k++){
				//Variable Setup.
				var otherName = nodeIncoming[k];
				var otherWeight = oldWeights[otherName];
				var otherOutgoing = outgoingEdges[otherName];
				var outgoingLength = otherOutgoing.length;
				if (outgoingLength==0){
					outgoingLength = num_nodes;
				}

				sumOut+=oldWeights[otherName]/outgoingLength;
			}			

			var PageRankResult = PageRankFormula(nodes.length, sumOut);
			if (PageRankResult > rankMax) rankMax = PageRankResult;
			if (PageRankResult < rankMin) rankMin = PageRankResult;
			currentWeights[node["id"]] = PageRankResult; 
		}


		//Clone the last object rather than simply copy a reference to it.
		var oldWeights = JSON.parse(JSON.stringify(currentWeights));
	}

	//Get the minimum and maximum PageRanks.

	//Set each node to have the value of its weight.
	for (var i=0; i < nodes.length ; i++){
		var node = nodes[i];
		//Scale each node so graph size doesn't affect the visuals too much.
		var scaledRank = (currentWeights[node["id"]]-rankMin)/rankMax
		node["value"] = scaledRank;
	}
}
