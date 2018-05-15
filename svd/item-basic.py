import sys
import time
from pymongo import MongoClient

def ratesort(x,y):
	if x['rate'] < y['rate']:
		return 1
	elif x['rate'] > y['rate']:
		return -1
	else:
		return 0
def valsort(x,y):
	if x['val'] < y['val']:
		return 1
	elif x['val'] > y['val']:
		return -1
	else:
		return 0

class itemRecommend(object):
	def __init__(self,userId):
		client = MongoClient('mongodb://localhost:27017/')
		db = client.movie_recommend
		users = db.users
		self.userData = users.find_one({'id':int(userId)})
		self.movies = db.movies

	def getRecommend(self):
		rate = self.userData['rates']
		rate.sort(ratesort)
		target = self.movies.find_one({'movieId':int(rate[0]['movieId'])})
		movieRate = []
		for row in self.movies.find({}):
			if(target['movieId'] == row['movieId']):
				continue
			else:
				union1 = list(set(target['cast']).intersection(set(row['cast'])))
				union2 = list(set(target['genres']).intersection(set(row['genres'])))
				union3 = list(set(target['production_companies']).intersection(set(row['production_companies'])))
				union4 = list(set(target['crew']).intersection(set(row['crew'])))
				val = (len(union1)+len(union2)*2+len(union3)+len(union4))*4 + row['vote_average']*0.3
				movieRate.append({
						'id':row['movieId'],
						'val':val
					})

		movieRate.sort(valsort)
		for i in range(0,len(movieRate)):
			sys.stdout.write(str(movieRate[i]['id'])+',')
			if(i > 4):
				break

if len(sys.argv) <= 1 :
	raise Exception,"Need one param"
else:
	r1 = itemRecommend(sys.argv[1])
	listData = r1.getRecommend()

