import csv
import json

entity={}
entitiesList=[]
wantedDirectors=['Stanley Kubrick','Robert Rodriguez','Quentin Tarantino','Rainer Werner Fassbinder',
                 'Francis Ford Coppola', 'Ethan Coen', 'Akira Kurosawa', 'Christopher Nolan', 'James Cameron',
                 'Martin Scorsese', 'Steven Spielberg', 'Ridley Scott','Woody Allen','Alfred Hitchcock',
                 'Tim Burton','David Lynch', 'Wes Anderson','Sergio Leone','Billy Wilder','Hayao Miyazaki'

]
wantedMovies=[]
with open('name.basics.tsv') as nameFile:
    next(nameFile) # skip headings
    reader=csv.reader(nameFile,delimiter='\t')
    for id, name, birthYear, deathYear,	primaryProfession, knownForTitles in reader:
        if name in wantedDirectors:
            # extracting the author
            entity= {'idIMDB' : id, 'name' : name, 'birthYear' : birthYear,  'deathYear' : deathYear,
                     'knownForTitles': knownForTitles }
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
           entity={'idIMDB': movies[0], 'title': movies[3], 'year': movies[5]}
           entitiesList.append(entity)
           if len(wantedMovies) == 0:  # Stop looking for movies once they have all been found
               break

with open('entitiesListIMDB.json','w') as outfile:
    json.dump(entitiesList, outfile)
