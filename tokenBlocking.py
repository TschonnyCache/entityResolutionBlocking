import json

with open('entitiesA.json') as json_file:
    entitiesList1 = json.load(json_file)

with open('entitiesB.json') as json_file:
    entitiesList2 = json.load(json_file)
datasets = [entitiesList1, entitiesList2]
# Tokens as keys and the value is a list of containing 
# the information of entities that have the token. 
# (dataset index and their index in the dataset)
blocks = dict()

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
		# This also applies if there is only one entity in the block
		if len(datasetsInBlock) == 1:
			blocksToRemove.append(block)
	for block in blocksToRemove:
		blocks.pop(block, None)

createTokenBlocks(datasets[0], 0)
createTokenBlocks(datasets[1], 1)
removeUnnecessaryBlocks()

# Output the blocks in to a json file
newBlocks = dict()
for block in blocks:
	blockList = []
	for entity in blocks[block]:
		blockList.append([entity['dataset'], entity['index']])
	newBlocks[block] = blockList

with open('blocks.json', 'w') as outfile:
    json.dump(newBlocks, outfile)


