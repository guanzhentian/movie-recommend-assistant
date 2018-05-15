# import sys
# import numpy
# from pymongo import MongoClient
# import csv

# client = MongoClient('mongodb://localhost:27017/')
# db = client.movie_recommend
# links = db.links

# reader = csv.reader(file('ml-latest-small/links.csv'))
# reader2 = csv.reader(file('save/id-to-movie.csv'))

# reader.next()
# movie = []
# link = {}

# for row in reader2:
# 	link[row[1]] = row[0]
# for row in reader:
# 	newData = {
# 	'movieId':row[0],
# 	'tmdbId':row[2],
# 	'id':link[row[0]]
# 	}
# 	movie.append(newData)

# result = links.insert_many(movie)
# print '-----------insert ',len(result),' --------'