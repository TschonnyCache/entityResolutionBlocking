import json

with open('entitiesListIMDB.json') as json_file:
    entitiesList1 = json.load(json_file)

with open('entitiesListIMDB.json') as json_file:
    entitiesList2 = json.load(json_file)

def extractAttributeNames(entitiesList):
    attributeNames = set() # set as we dont want duplicates
    for entity in entitiesList:
        for key in entity:
            attributeNames.add(key)
    # attributeNames are dicts with the names as keys and as value a list with the values that occur in this attribute
    attributeAnnotatedDict = dict()
    for attributeName in attributeNames:
        attributeAnnotatedDict[attributeName] = list()
    # collecting the values for the attribute names

    for entity in entitiesList :
        for attributeName in entity:
            attributeAnnotatedDict[attributeName].append(entity.get(attributeName))
    return attributeAnnotatedDict

def numberOfCommonElements(list1, list2):
     return len(list(set(list1) & set(list2)))

def cardinalityOfUnion(list1,list2):
    return len(list(set(list1).union(set(list2))))

def jaccardSimilarity(valueList1, valueList2):
    return numberOfCommonElements(valueList1,valueList2) / cardinalityOfUnion(valueList1,valueList2)

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
        links[attributeName] = mostSimilarAttribute
    return links

# extracting attribute names
attributeNames1 = extractAttributeNames(entitiesList1)
attributeNames2 = extractAttributeNames(entitiesList2)
links1to2 = createLinks(attributeNames1,attributeNames2)
links2to1 = createLinks(attributeNames2,attributeNames1)

print links2to1

# computing most similar attributes
