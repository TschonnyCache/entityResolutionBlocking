import json
import requests

#split the string from the last '/' and clean the key or value
def urlSplitter(key):
	i = len(key) - 1
	while i > 0:
		if key[i] == '/':
			return key[i+1:]
		i = i - 1
	return key

wanted_movies = ['Blade_Runner_2049', 'A_Clockwork_Orange_(film)']

for movie in wanted_movies:
	r = requests.get('http://dbpedia.org/data/' + movie + '.jsod')
	data = r.json()['d']['results'][0]
	print('Movie name: ' + movie)
	for key in data:
		# logic used to select fitting key value pairs
		if ('ontology' in key or 'property' in key) and 'abstract' not in key and 'wiki' not in key:
			cleaned_key = urlSplitter(key)
			value = ""
			if type(data[key]) is dict:
				value = urlSplitter(data[key]['__deferred']['uri'])
			else:
				value = data[key]
			print(cleaned_key + ' ' + value)