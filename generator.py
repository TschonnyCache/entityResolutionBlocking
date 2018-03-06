# this python script is used to generate 2 entity lists for the token and attributeclusteringblocking
import random
import json

entitiesA = []
entitiesB = []

for i in range(125):
    entityA = {str(random.randint(100, 125)): str(random.randint(0, 50)), 
                str(random.randint(175, 200)): str(random.randint(100, 200)), 
                str(random.randint(201, 225)): str(random.randint(5000, 15000))}
    entityB = {str(random.randint(100, 125)): str(random.randint(0, 50)), 
                str(random.randint(175, 200)): str(random.randint(100, 200)), 
                str(random.randint(201, 225)): str(random.randint(5000, 15000))}
    if entityA not in entitiesA and entityB not in entitiesB:
        entitiesA.append(entityA)
        entitiesB.append(entityB)
    if i < 15:
        entitiesA.append(entityB)
        entitiesB.append(entityA)

with open('entitiesA.json','w') as outfile:
    json.dump(entitiesA, outfile)
with open('entitiesB.json','w') as outfile:
    json.dump(entitiesB, outfile)