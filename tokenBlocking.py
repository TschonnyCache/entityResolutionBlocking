import json
import pdb

with open('entitiesA.json') as json_file:
    entitiesList1 = json.load(json_file)

with open('entitiesB.json') as json_file:
    entitiesList2 = json.load(json_file)
datasets = [entitiesList1, entitiesList2]
# Tokens as keys and the value is a list of containing 
# the information of entities that have the token. 
# (dataset index and their index in the dataset)
blocks = dict()
# The similarties that have already been calculated.
# Key is a tuple with the information of the 2 compared entities, value is the similarity
similarities = dict()

def numberOfCommonElements(list1, list2):
     return len(list(set(list1) & set(list2)))

def cardinalityOfUnion(list1,list2):
    return len(list(set(list1).union(set(list2))))

def jaccardSimilarity(valueList1, valueList2):
    return numberOfCommonElements(valueList1,valueList2) / cardinalityOfUnion(valueList1,valueList2)

def createTokenBlocks(dataset, dataset_index):
	index = 0
	while index < len(dataset):
		entity = dataset[index]
		for attribute in entity:
			# A block is created for every token
			if entity[attribute] in blocks:
				blocks[entity[attribute]].append(dict(dataset=dataset_index, index=index))
			else:
				blocks[entity[attribute]] = [dict(dataset=dataset_index, index=index)]
		index += 1

def removeUnnecessaryBlocks():
	blocksToRemove = []
	for block in blocks:
		datasetsInBlock = []
		for entity in blocks[block]:
			if entity['dataset'] not in datasetsInBlock:
				datasetsInBlock.append(entity['dataset'])
		# If all the entities in the block are from the same dataset
		if len(datasetsInBlock) == 1:
			blocksToRemove.append(block)
	for block in blocksToRemove:
		blocks.pop(block, None)

def calculateSimilarities():
	for block in blocks:
		for entity in blocks[block]:
			for secondEntity in blocks[block]:
				# create the tuple that acts as a key for "similarities"
				tupleKey = (entity['dataset'], entity['index'], secondEntity['dataset'], secondEntity['index'])
				# calculate the similarity for the entities
				if entity is not secondEntity and tupleKey not in similarities and entity['dataset'] != secondEntity['dataset']:
					# calculate the similarity for the entities
					# jaccardSimilarity is given lists of the two entities values
					similarity = jaccardSimilarity(datasets[entity['dataset']][entity['index']].values(), 
													datasets[secondEntity['dataset']][secondEntity['index']].values())
					similarities[tupleKey] = similarity

createTokenBlocks(datasets[0], 0)
createTokenBlocks(datasets[1], 1)
removeUnnecessaryBlocks()

newBlocks = dict()
for block in blocks:
	blockList = []
	for entity in blocks[block]:
		blockList.append([entity['dataset'], entity['index']])
	newBlocks[block] = blockList

with open('blocks.json', 'w') as outfile:
    json.dump(newBlocks, outfile)


