import json

with open('entitiesListIMDB.json') as json_file:
    entitiesList1 = json.load(json_file)

with open('entitiesListIMDB.json') as json_file:
    entitiesList2 = json.load(json_file)

# extracting attribute names
# attributeNames are dicts with the names as keys and as value a list with the values that occur in this attribute
def extractAttributeNames(entitiesList):
    attributeNames = set() # set as we dont want duplicates
    for entity in entitiesList:
        for key in entity:
            attributeNames.add(key)
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

attributeNames1 = extractAttributeNames(entitiesList1)
attributeNames2 = extractAttributeNames(entitiesList2)