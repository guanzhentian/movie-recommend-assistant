import csv
import time
from pymongo import MongoClient
from svd import svd

class update_rate(object):
	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client.movie_recommend
		self.rates = self.db.rates
		self.links = self.db.links

	def  update(self):
		out  = open('../svd/ml-latest-small/ratings.csv','ab')
		csv_writer = csv.writer(out,dialect = "excel")
		data = self.rates.find({})
		num = 0;
		for i in range(0,self.rates.count()):
			value = data[i]
			mid = self.links.find_one({'tmdbId':str(value['movieId'])});
			if mid:
				num+=1
				row = [value['userId'],mid['movieId'],value['rate'],value['time']]
				csv_writer.writerow(row)
			else:
				print mid
		print '--------update number  ',num,' ---------------'
		out.close();
		return num

	def clean(self):
		print '--------current number of data ',self.rates.count(),' ---------------'
		result = self.rates.delete_many({})
		print '--------clean number  ',result.deleted_count,' ---------------'	

starttime = time.time()
u = update_rate()
num = u.update()
u.clean()

alpha = 0.003
lamba = 0.01
if num >0:
	svd2 = svd(3,  alpha, lamba,30)
	svd2.printData()
	svd2.saveData()
else:
	print '------------no update data,no svd-------------------------'

endtime = time.time()
print '\n-----------update ratings data fininshed ,cost time %f -------------\n'% (endtime - starttime)