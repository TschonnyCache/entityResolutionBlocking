import csv
import json

wantedDirectors=['Stanley Kubrick','Robert Rodriguez','Quentin Tarantino','Rainer Werner Fassbinder',
                 'Francis Ford Coppola', 'Ethan Coen', 'Akira Kurosawa', 'Christopher Nolan', 'James Cameron',
                 'Martin Scorsese', 'Steven Spielberg', 'Ridley Scott','Woody Allen','Alfred Hitchcock',
                 'Tim Burton','David Lynch', 'Wes Anderson','Sergio Leone','Billy Wilder','Hayao Miyazaki'
]

wantedDirectors2=['Stanley Kubrick','Robert Rodriguez','Quentin Tarantino','Rainer Werner Fassbinder',
                 'Francis Ford Coppola', 'Ethan Coen', 'Steven Spielberg', 'Ridley Scott','Woody Allen',
                 'Alfred Hitchcock', 'Tim Burton','David Lynch', 'Jim Jarmusch', 'Oliver Stone', 'Mike Judge',
                 'Joel Coen', 'Buster Keaton', 'Roman Polanski', 'Peter Jackson', 'Mel Brooks'
]

fileName = 'entitiesListIMDB.json'
fileName2 = 'entitiesListAlternate.json'

attributeNames=['idIMDB','name','birthYear','deathYear', 'knownForTitles', 'year']
attributeNames2=['idAlt','label','yearOfBirth','yearOfDeath','knownFor','year']

def doExtraction(wantedDirectors, fileName, attList):
    entity = {}
    entitiesList = []
    wantedMovies = []

    with open('name.basics.tsv') as nameFile:
        next(nameFile) # skip headings
        reader=csv.reader(nameFile,delimiter='\t')
        for id, name, birthYear, deathYear,	primaryProfession, knownForTitles in reader:
            if name in wantedDirectors:
                # extracting the author
                entity= {attList[0] : id, attList[1] : name, attList[2] : birthYear,  attList[3] : deathYear,
                         attList[4]: knownForTitles }
                entitiesList.append(entity)
                wantedDirectors.remove(name) # There were several duplicate names but the 'famous' people have the lower id
                                            # and therefore appear first in the files

                # extracting the movies s/he is famous for
                knownFor = knownForTitles.split(",")
                wantedMovies.extend(knownFor) # Collecting the movies from the current director in the to query list
                if len(wantedDirectors) == 0: # Stop looking for directors once they have all been found
                    break

    with open('title.basics.tsv') as moviesFile:
        next(moviesFile) # skip headings
        reader = csv.reader(moviesFile, delimiter='\t', quoting=csv.QUOTE_NONE) #QUOTE_NONE "Instructs reader to perform no
                                                                                #  special processing of quote characters"
        for movies in reader:
            if movies[0] in wantedMovies:
               entity={attList[0]: movies[0], attList[1]: movies[3], attList[5]: movies[5]}
               entitiesList.append(entity)
               if len(wantedMovies) == 0:  # Stop looking for movies once they have all been found
                   break

    with open(fileName,'w') as outfile:
        json.dump(entitiesList, outfile)

doExtraction(wantedDirectors,fileName,attributeNames)
doExtraction(wantedDirectors2,fileName2,attributeNames2)