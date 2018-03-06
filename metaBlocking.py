import json
import itertools
import math
import pdb

with open('entitiesA.json') as json_file:
    entitiesList1 = json.load(json_file)

with open('entitiesB.json') as json_file:
    entitiesList2 = json.load(json_file)
datasets = [entitiesList1, entitiesList2]

with open('blocks.json') as json_file:
    blocks = json.load(json_file)

nodes=[]
edges=[]
edgeWeights = dict()

# graph building
for block in blocks:
    # Add all the entities from the blocks in to 'nodes'
    for entity in blocks[block]:
        if not entity in nodes:
            nodes.append(entity)
    # Get all permutations of 2 entities from a block
    permutations = itertools.permutations(blocks[block],2)
    for permutation in permutations:
        # Create a nondirected edge for each permutation using 'set()'
        edge = {tuple(permutation[0]),tuple(permutation[1])}
        # Add each nondirected edge in to 'edges' once
        if len(edge) == 2 and edge not in edges:
            # this is why we have edges as sets
            edges.append(edge)

# How many common blocks 2 entities share
def getNumberOfCommonBlocks(edge):
    counter = 0
    entities = list(edge)
    for block in blocks:
        entitiesList = blocks[block]
        if list(entities[0]) in entitiesList and list(entities[1]) in entitiesList:
            counter += 1
    return counter

# Blocking scheme where the edges are weighted based 
# on the common blocks between the entities in each node.
def commonBlockScheme():
    for edgeIndex, edge in enumerate(edges):
        edgeWeights[edgeIndex]=getNumberOfCommonBlocks(edge)

# How many blocks is an entity in
def getNumberOfBlocksForEntity(entity):
    counter = 0
    for block in blocks:
        entitiesList = blocks[block]
        if list(entity) in entitiesList:
            counter += 1
    return counter

# Blocking scheme where the edges are weighted based 
# on how similar 2 entities are when looking at their blocks
def jaccardScheme():
    for edgeIndex, edge in enumerate(edges):
        entities = list(edge)
        numberOfCommonBlocks=getNumberOfCommonBlocks(edge)
        numOfA = getNumberOfBlocksForEntity(entities[0])
        numOfB = getNumberOfBlocksForEntity(entities[1])
        weight = float(numberOfCommonBlocks) / float( numOfA + numOfB - numberOfCommonBlocks)
        edgeWeights[edgeIndex] = weight

def getAverageEdgeWeightOfGraph():
    averageWeight = 0
    for weight in edgeWeights:
        averageWeight += edgeWeights[weight]
    numberOfWeights= float(len(edgeWeights))
    averageWeight = float(averageWeight) / numberOfWeights
    return averageWeight

# Pruning method where edges are removed
# if their weight is below average
def weightEdgePruning():
    averageWeight = getAverageEdgeWeightOfGraph()
    for edgeIndex, weight in edgeWeights.iteritems():
        if weight < averageWeight:
            edges[edgeIndex] = None

def getWeightedNeighborhood(node):
    # creating a list of the neighboring edges with tuples of the edge index in the main
    # edge list and its weight
    neighborEdgesIndices = []
    for index, edge in enumerate(edges):
        if tuple(node) == list(edge)[0]:
            neighborEdgesIndices.append((index,edgeWeights[index]))
        elif tuple(node) == list(edge)[1]:
            neighborEdgesIndices.append((index,edgeWeights[index]))
    return neighborEdgesIndices

def calculateBlockingCardinality():
    blockingCardinality = 0
    for block in blocks:
        blockingCardinality += len(blocks[block])
    return float(blockingCardinality) / float(len(nodes))

def calculateK(blockingCardinality):
    return int(math.floor(blockingCardinality-1))

def calculateLocalK(neighborhood):
    cardinalityOfEdges = len(neighborhood)
    k = int(math.ceil(0.1*cardinalityOfEdges))
    return k

def cardinalityNodePruning():
    directedEdges = []

    for node in nodes:
        # getting all neighboring edges and their weights
        neighborEdgeIndexAndWeights = getWeightedNeighborhood(node)
        # get k
        k = calculateLocalK(neighborEdgeIndexAndWeights)
        print("neigborhood " + str(len(neighborEdgeIndexAndWeights)) + " k " + str(k))
        # sorting the neighboring edges by their weight
        neighborEdgeIndexAndWeights = sorted(neighborEdgeIndexAndWeights,key=lambda weight: weight[1], reverse=True)
        # selecting the top k edges
        topKEdgeIndexAndWeights = neighborEdgeIndexAndWeights[:k]
        # creating a directed edge for every top k edge
        for edgeIndexAndWeight in topKEdgeIndexAndWeights:
            # from the original edges list, take the top k indices we just computed
            originalEdge = list(edges[edgeIndexAndWeight[0]])
            # checking if the root of the edge is the node we are analysing
            if originalEdge[0] == tuple(node):
                directedEdges.append(originalEdge)
            else:
                originalEdge.reverse()
                directedEdges.append(originalEdge)
    return directedEdges

# Collect the new blocks based on the graph from cardinality node pruning.
# A block is created by taking a nodes directed edges 
# and combining the nodes that are pointed at in to a block.
def collectDirecterGraphBlocks(directedEdges):
	directedBlocks = dict()
	for edge in directedEdges:
		# if the origin node of the arrow already has a block
		if edge[0] in directedBlocks:
			directedBlocks[edge[0]].append(edge[1])
		# create a new block for the edges origin node
		else:
			directedBlocks[edge[0]] = [edge[1]]
	return directedBlocks

def updateNeighbourhood(node1, node2, neighbourhood):
	if node1 in neighbourhood:
		neighbourhood[node1].append(node2)
	else:
		neighbourhood[node1] = [node2]
	return neighbourhood

def recursiveBlockCollector(node, neighbourhood, usedNodes):
	block = []
	if node not in usedNodes:
		block.append(node)
		usedNodes.append(node)
		for innerNode in neighbourhood[node]:
			innerBlock, usedNodes = recursiveBlockCollector(innerNode, neighbourhood, usedNodes)
			block += innerBlock
	return block, usedNodes

# Collect the blocks based the the graph from weighted edge pruning.
# Blocks are created by following the edges in the graph.
def collectGraphBlocks():
	resultBlocks = []
	# list of the nodes that have already been added to blocks
	usedNodes = []
	neighbourhood = dict()
	# lets get the whole neighbourhood for all nodes
	for index, edge in enumerate(edges):
		if edge is not None:
			# add entries for the nodes or update with new neighbours
			neighbourhood = updateNeighbourhood(list(edge)[0], list(edge)[1], neighbourhood)
			neighbourhood = updateNeighbourhood(list(edge)[1], list(edge)[0], neighbourhood)
	# Iterate over nodes, 
	# and if the node is not in any of the blocks, 
	# create a new block for it and its neighbours.
	for node in neighbourhood:
		if node not in usedNodes:
			newBlock, usedNodes = recursiveBlockCollector(node, neighbourhood, usedNodes)
			resultBlocks.append(newBlock)
	return resultBlocks

def printNumberOfEdgesPerNode():
    for node in nodes:
        numberOfEdges = 0
        for edge in edges:
            if tuple(node) == list(edge)[0]:
                numberOfEdges += 1
            elif tuple(node) == list(edge)[1]:
                numberOfEdges += 1
        print(numberOfEdges)

# Weighting schemes
#commonBlockScheme()
jaccardScheme()

# Pruning schemes
directedEdges = cardinalityNodePruning()
weightEdgePruning()

# Collecting the new blocks
directedResultBlocks = collectDirecterGraphBlocks(directedEdges)
resultBlocks = collectGraphBlocks()

print "Result of cardinality node pruning, amount of blocks: " + str(len(directedResultBlocks))
for block in directedResultBlocks:
    if len(directedResultBlocks[block]) > 1:
        print directedResultBlocks[block]
print "Result of weight edge pruning, amount of blocks: " + str(len(resultBlocks))
print resultBlocks