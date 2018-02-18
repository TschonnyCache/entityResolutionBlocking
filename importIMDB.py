import csv

directors=[]
ids=[]
wantedDirectors=['Stanley Kubrick','Robert Rodriguez','Quentin Tarantino','Rainer Werner Fassbinder',
                 'Francis Ford Coppola', 'Ethan Coen', 'Akira Kurosawa', 'Christopher Nolan', 'James Cameron',
                 'Martin Scorsese']
with open('name.basics.tsv') as nameFile:
    next(nameFile) # skip headings
    reader=csv.reader(nameFile,delimiter='\t')
    for id, name, birthYear, deathYear,	primaryProfession, knownForTitles in reader:
        if name in wantedDirectors:
            print id + ' ' + name + ' ' + birthYear + ' ' + deathYear + ' ' + primaryProfession + ' ' + knownForTitles