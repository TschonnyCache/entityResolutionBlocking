import json
import itertools
import math

with open('entitiesListIMDB.json') as json_file:
    entitiesList1 = json.load(json_file)

with open('entitiesListAlternate.json') as json_file:
    entitiesList2 = json.load(json_file)
datasets = [entitiesList1, entitiesList2]

with open('tokenBlockingResult.json') as json_file:
    blocks = json.load(json_file)

nodes=[]
edges=[]
edgeWeights = dict()

#graph building
for block in blocks:
    for entity in blocks[block]:
        if not entity in nodes:
            nodes.append(entity)
    permutations = itertools.permutations(blocks[block],2)
    for permutation in permutations:
        edge = {tuple(permutation[0]),tuple(permutation[1])}
        if edge not in edges:
            # this is why we have edges as sets
            edges.append(edge)

def getNumberOfCommonBlocks(edge):
    counter = 0
    entities = list(edge)
    for block in blocks:
        entitiesList = blocks[block]
        if list(entities[0]) in entitiesList and list(entities[1]) in entitiesList:
            counter += 1
    return counter

def commonBlockScheme():
    for edgeIndex, edge in enumerate(edges):
        edgeWeights[edgeIndex]=getNumberOfCommonBlocks(edge)

def getNumberOfBlocksForEntity(entity):
    counter = 0
    for block in blocks:
        entitiesList = blocks[block]
        if list(entity) in entitiesList:
            counter += 1
    return counter

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

def cardinalityNodePruning():
    directedEdges = []
    bC = calculateBlockingCardinality()
    k = calculateK(bC)
    for node in nodes:
        # getting all neighboring edges and their weights
        neighborEdgeIndexAndWeights = getWeightedNeighborhood(node)
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

#Weighting schemes
#commonBlockScheme()
jaccardScheme()
#weightEdgePruning()
directedEdges = cardinalityNodePruning()



