import json

with open('entitiesListIMDB.json') as json_file:
    entitiesList1 = json.load(json_file)

with open('entitiesListAlternate.json') as json_file:
    entitiesList2 = json.load(json_file)
datasets = [entitiesList1, entitiesList2]

# create a list of attribute names, annotated with the occuring values
def extractAttributeNames(entitiesList, datasetIndex):
    attributeNames = set() # set as we dont want duplicates
    for entity in entitiesList:
        for key in entity:
            # Using tuple made of the attribute name and the dictionary index as key
            attributeNames.add((key,datasetIndex))
    # attributeAnnotatedDict are dicts with the attribute names dictionary index as keys (in a tuple) and
    # as value a list with the values that occur in this attribute
    attributeAnnotatedDict = dict()
    for attributeName in attributeNames:
        attributeAnnotatedDict[attributeName] = list()

    # collecting the values for the attribute names
    for entity in entitiesList :
        for attributeName in entity:
            attributeAnnotatedDict[(attributeName,datasetIndex)].append(entity.get(attributeName))
    return attributeAnnotatedDict

def numberOfCommonElements(list1, list2):
     return len(list(set(list1) & set(list2)))

def cardinalityOfUnion(list1,list2):
    return len(list(set(list1).union(set(list2))))

def jaccardSimilarity(valueList1, valueList2):
    return float(numberOfCommonElements(valueList1,valueList2))  / float(cardinalityOfUnion(valueList1,valueList2))

def getMostSimilarAttribute(attribute,setOfAttributes, setOfOtherAttributes):
    mostSimilarAttribute = 0
    highestSimilarity = 0
    for otherAttribute in setOfOtherAttributes:
        similarity = jaccardSimilarity(setOfAttributes[attribute],setOfOtherAttributes[otherAttribute])
        if similarity > highestSimilarity:
            highestSimilarity = similarity
            mostSimilarAttribute = otherAttribute
    return mostSimilarAttribute

def createLinks(attributeNames1, attributeNames2):
    links = {}
    for attributeName in attributeNames1:
        mostSimilarAttribute = getMostSimilarAttribute(attributeName,attributeNames1,attributeNames2)
        if not mostSimilarAttribute == 0:
            links[attributeName] = mostSimilarAttribute
    return links

def computeTransitiveClosure(links1to2, links2to1,listOfClusters):
    # cases:
    # attributes point towards ech other.
    # there are no links pointing towards the current attribute
    # there are links pointing towards the current attribute, that have to be adde to the set later.
    sideBool = True
    for root in links1to2:
        # creating a set from the current root
        target = links1to2[root]
        currentCluster = {root, target}
        while True:
            foundOtherCluster = False
            # get next target
            # would be nice to have the origin of a certain attribute
            if sideBool:
                target = links2to1[target]
            else:
                target = links1to2[target]

            # checking if there a superset cluster exists
            for index, cluster in enumerate(listOfClusters):
                # the current attribute links to a existing cluster
                if target in cluster:
                    # adding the current cluster to the existing one
                    listOfClusters[index] = cluster.union(currentCluster)
                    foundOtherCluster = True
                    break
            if foundOtherCluster:
                break

            # link points to an attribute that allready is in the current cluster
            if target in currentCluster:
                listOfClusters.append(currentCluster)
                break

            sideBool = not sideBool
            root = target

    return listOfClusters

def computeTransitiveClosureWrapper(links1to2, links2to1):
    listOfClusters = []
    listOfClusters = computeTransitiveClosure(links1to2,links2to1,listOfClusters)
    listOfClusters = computeTransitiveClosure(links1to2,links2to1,listOfClusters)
    return  listOfClusters

def cleanClusters(listOfClusters):
    glueCluster = set
    for cluster in listOfClusters:
        if len(cluster) == 1:
            glueCluster = glueCluster.union(cluster)
            listOfClusters.remove(cluster)
    return listOfClusters

def createBlocksfromClusters(listOfClusters,attributeNames,attributeNames2):
    attributeNames.update(attributeNames2)
    blocks = dict()
    for clusterIndex, cluster in enumerate(listOfClusters):
        for attribute in cluster:
            for value in attributeNames[attribute]:
                for datasetIndex, dataset in enumerate(datasets):
                    for entityIndex, entity in enumerate(dataset):
                        if attribute[0] in entity:
                            if entity[attribute[0]] == value:
                                # next(iter(cluster))[0] is the name of the first attribute in the cluster
                                key = 'C' + unicode(clusterIndex) + '.' + value
                                value = (datasetIndex,entityIndex)
                                if key in blocks:
                                    if not value in blocks[key]:
                                        blocks[key].append(value)
                                else:
                                    blocks[key]= [value]

    #removing blocks of size 1
    fliterdBlocks = dict()
    for block, entities in blocks.iteritems():
        if not len(entities) == 1:
            fliterdBlocks[block]=entities

    return fliterdBlocks

# extracting attribute names and computing most similar attributes
attributeNames1 = extractAttributeNames(entitiesList1,1)
attributeNames2 = extractAttributeNames(entitiesList2,2)
# creating links between attributes
links1to2 = createLinks(attributeNames1,attributeNames2)
links2to1 = createLinks(attributeNames2,attributeNames1)
#creating the transitive closure
listOfClusters = computeTransitiveClosureWrapper(links1to2, links2to1)
cleanListOfClusters = cleanClusters(listOfClusters)
blocks = createBlocksfromClusters(cleanListOfClusters,attributeNames1,attributeNames2)
with open('attributeClusteringBlockingResult.json', 'w') as outfile:
    json.dump(blocks, outfile)
