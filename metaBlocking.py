import json
import itertools

with open('entitiesListIMDB.json') as json_file:
    entitiesList1 = json.load(json_file)

with open('entitiesListAlternate.json') as json_file:
    entitiesList2 = json.load(json_file)
datasets = [entitiesList1, entitiesList2]

with open('attributeClusteringBlockingResult.json') as json_file:
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

commonBlockScheme()
print("a")


