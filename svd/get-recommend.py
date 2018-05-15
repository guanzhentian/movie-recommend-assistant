import sys
import numpy
import time
import csv
from pymongo import MongoClient

def sort(x,y):
	if x['rate'] < y['rate']:
		return 1
	elif x['rate'] > y['rate']:
		return -1
	else:
		return 0

class recommend(object):
	"""docstring for recommend"""
	def __init__(self,userId):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client.movie_recommend
		self.id_user = self.db.userlinks
		self.links = self.db.links
		self.users = self.db.users


		self.basicDataDir = '../svd/save/'

		self.bu = None
		self.bi = None
		self.p = None
		self.q = None
		self.avg = None
		self.id = None
		self.userId = userId
		self.rate = None

		self.initBuBi()
		self.initAvg()
		self.initId()
		self.initPQ()
		self.calc()


	def initBuBi(self):
		buReader = csv.reader(file(self.basicDataDir +'bu.csv'))
		biReader = csv.reader(file(self.basicDataDir + 'bi.csv'))
		bu = []
		bi = []
		for row in buReader:
			bu.append(float(row[0]))
		for row in biReader:
			bi.append(float(row[0]))

		self.bu = bu
		self.bi = bi
		# print '------------init Bu Bi ',len(bu),len(bi),'--------------'

	def initAvg(self):
		file2 = open(self.basicDataDir +'avg.txt','r')
		self.avg = float(file2.read())
		file2.close()
		# print '---------self avg init ',self.avg,'-------------'

	def initId(self):
		idData = self.id_user.find_one({'userId':str(self.userId)})
		self.id = idData['id']
		# print '------------init ID ',self.id,'--------------'

	def initPQ(self):
		qReader = csv.reader(file(self.basicDataDir +'q.csv'))
		pReader = csv.reader(file(self.basicDataDir + 'p.csv'))
		q = []
		p = []
		for row in qReader:
			q.append(row)
		for row in pReader:
			p.append(row)

		self.p =  numpy.array([p[self.id]],dtype = numpy.float64)
		self.q = numpy.array(q ,dtype = numpy.float64)
		# print '--------init P Q ,',self.p.shape,self.q.shape,'----------'

	def calc(self):
		data = numpy.matmul(self.p,self.q)
		a = data.shape
		rate = []
		for i in range(0,a[1]):
			# i = movieId
			# 
			val = data[0,i] + self.avg + self.bu[self.id] + self.bi[i]
			rate.append({
					'id':i,
					'rate':float(val),
					'bool':True
				})

		self.rate = rate

	def getList(self):
		userdata = self.users.find_one({'id':int(self.userId)})
		for item in userdata['rates']:
			md = self.links.find_one({'tmdbId':str(item['movieId'])})
			if md:
				self.rate[int(md['id'])]['bool'] = False

		self.rate.sort(sort)
		num = 0
		idlist = []
		for i in range(0,len(self.rate)):
			if self.rate[i]['bool']:
				md = self.links.find_one({'id':str(self.rate[i]['id'])})
				idlist.append(md['tmdbId']) 
				num += 1
				if(num >= 5):
					break;

		return idlist


if len(sys.argv) <= 1 :
	raise Exception,"Need one param"
else:
	r1 = recommend(sys.argv[1])
	listData = r1.getList()
	for i in listData:
		sys.stdout.write(i+',')
# print '\n-----------csv data load finished ,cost time %f -------------\n'% (endtime - starttime)