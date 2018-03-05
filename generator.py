# this python script is used to generate 2 entity lists for the token and attributeclusteringblocking
import random
import json

entitiesA = []
entitiesB = []

for i in range(125):
	entityA = {str(random.randint(100, 150)): str(random.randint(0, 50)), 
				str(random.randint(151, 200)): str(random.randint(100, 200)), 
				str(random.randint(201, 250)): str(random.randint(5000, 15000))}
	entityB = {str(random.randint(100, 150)): str(random.randint(0, 50)), 
				str(random.randint(151, 200)): str(random.randint(100, 200)), 
				str(random.randint(201, 250)): str(random.randint(5000, 15000))}
	if entityA not in entitiesA and entityB not in entitiesB:
		entitiesA.append(entityA)
		entitiesB.append(entityB)

with open('entitiesA.json','w') as outfile:
	json.dump(entitiesA, outfile)
with open('entitiesB.json','w') as outfile:
	json.dump(entitiesB, outfile)