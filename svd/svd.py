import csv
import numpy
import time
from pandas import DataFrame
import os 
from pymongo import MongoClient

class svd(object):
	"""docstring for svd 0.005 0.02"""
	def __init__(self, ndim ,alpha ,lamba ,times ):
		self.basicDataDir = '../svd/ml-latest-small'
		dataname = self.basicDataDir+'/ratings.csv'
		  
		
		self.ndim = ndim 		
		self.test_proportion = 0.001
		self.user_rate_data = None

		# self.martix = numpy.array(y,dtype = numpy.float64) 
		# maxdata = self.martix.max(axis = 0)
		# self.user = int(maxdata[0]) 	
		self.user = None
		self.avgRate = None
		self.movieData = None
		self.movie = None
		self.p = None
		self.q = None
		self.bu = None
		self.bi = None
		self.trainData = None
		self.testData = None
		self.alpha = alpha
		self.lamba = lamba
		self.circleTime = times
		self.trainRmse = None
		self.testRmse = None
		self.compareData = None
		self.id_to_movie = None
		self.user_to_id = None

		self.handleCsvData(dataname,True)
		self.handleUserData()
		self.handleMovieData()
		self.initData()
		self.train()
		self.test()

	def handleUserData(self):
		num = 0
		obj = {}
		userlist = []
		for row in self.user_rate_data:
			if obj.has_key(str(row[0])):
				continue
			else:
				obj[str(row[0])] = num
				newData ={
					'id':num,
					'userId':row[0]
				}
				num +=1
				userlist.append(newData)
		self.user = num
		self.user_to_id = obj
		client = MongoClient('mongodb://localhost:27017/')
		db = client.movie_recommend
		userlinks = db.userlinks
		userlinks.delete_many({})
		userlinks.insert_many(userlist)
		print '\n-----------User data init finished  -------------\n'
		print '----------',self.user,'---------------------'


	def handleCsvData(self,name,skip=False):
		starttime = time.time()
		reader = csv.reader(file(name))
		if skip:
			reader.next()
		allRow = []
		for row in reader:
			row.pop()
			allRow.append(row)
		endtime = time.time()
		print '\n-----------csv data load finished ,cost time %f -------------\n'% (endtime - starttime)
		self.user_rate_data =  allRow	

	def  handleMovieData(self):
		starttime = time.time()
		link = self.basicDataDir+'/movies.csv'
		reader = csv.reader(file(link))
		reader.next()
		md = {}
		# itm = []
		num = 0
		for row in reader:
			newData = {
				'title':row[1],
				'genres':row[2],
				'id':num
			}
			# newData2 = [num,row[0]]
			md[row[0]] = newData
			# itm.append(newData2)
			num+=1

		# self.id_to_movie = numpy.array(itm)
		self.movie =len(md)
		self.movieData =  md
		endtime = time.time()
		print '-----------movie data load finished,cost time %f   -----------------\n'% (endtime - starttime)

	def initData(self):
		starttime = time.time()

		#get train data & test data
		numPop = int(self.test_proportion *len(self.user_rate_data))
		testData = []
		for i in range(0,numPop):
			ran = numpy.random.randint(0,len(self.user_rate_data))
			td = self.user_rate_data.pop(ran)
			testData.append(td)
		self.testData = testData
		self.trainData = self.user_rate_data

		#get rate avg
		rateSum = 0.0
		for item in self.trainData:
			rateSum += float(item[2])
		rateSum /= len(self.trainData)
		self.avgRate = rateSum

		#init p
		userArray = []
		for i in range(0,self.user):
			row = []
			for j in range(0,self.ndim):
				rd = numpy.random.uniform(0,1)
				# rd = 0
				row.append(rd)
			userArray.append(row)

		self.p = numpy.array(userArray,dtype = numpy.float64)

		#init q
		itemArray = []
		for i in range(0,self.ndim):
			row = []
			for j in range(0,self.movie):
				rd = numpy.random.uniform(0,1)
				# rd = 0
				row.append(rd)
			itemArray.append(row)

		self.q = numpy.array(itemArray,dtype = numpy.float64) 
		#init bu bi
		bu = []
		bi = []
		for i in range(0,self.user):
			bu.append(0)
		for i in range(0,self.movie):
			bi.append(0)
		self.bu = bu
		self.bi =bi
		


		endtime = time.time()
		print '-----------initData finished,cost time %f   -----------------\n'% (endtime - starttime)

	def train(self):
		times = self.circleTime
		starttime = time.time()
		lastRmse = float(10000.0)
		for k in range(0,times):
			rmse = 0
			rmseNum = 0
			for item in self.trainData:
				user = self.user_to_id[str(item[0])]
				movie = str(item[1])
				rui = float(item[2])
				try:
					rui2 = self.avgRate + self.bu[user] + self.bi[self.movieData[movie]['id']] + numpy.matmul(self.p[user],self.q[:,self.movieData[movie]['id']])				
				except:
					print '----------error user ',user
					print '----------error movie ',movie
					print '----------error type(movie) ',type(movie)
					print '----------error self.movieData[movie] ',self.movieData[movie]
				# if rui2 > 5:
				# 	rui2  = 5
				# elif rui2 < 0:
				# 	rui2 = 0
				e = float(rui) - float(rui2)
				#train
				self.bu[user] += self.alpha*(e - self.lamba * self.bu[user])
				self.bi[self.movieData[movie]['id']] += self.alpha*(e - self.lamba * self.bi[self.movieData[movie]['id']])
				for i in range(0,self.ndim):
					# print self.alpha*(e*self.q[i,self.movieData[movie]['id']] - self.lamba * self.p[user,i])
					self.p[user,i] += self.alpha*(e*self.q[i,self.movieData[movie]['id']] - self.lamba * self.p[user,i])
					self.q[i,self.movieData[movie]['id']] += self.alpha*(e*self.p[user,i] - self.lamba * self.q[i,self.movieData[movie]['id']])
				rmse += e * e
				rmseNum += 1
			# self.alpha *= 0.9
			# print (rmse,rmseNum)
			rmse = ((rmse/rmseNum)**0.5)

			# try:
			# 	print  '----------------%d Train RMSE = %f -------------------------'% (k,float(rmse))
			# except:
			# 	print("Unexpected error")

			if rmse > lastRmse:
				print '----------------%d Train RMSE up-------------------------' % k
				break
			else:
				lastRmse = rmse
		self.trainRmse = rmse	
		# endtime = time.time()
		# print '-----------initData finished,cost time %f   -----------------\n'% (endtime - starttime)

	def test(self):
		starttime = time.time()
		rmse = 0
		rmseNum = 0
		ruilist = []

		for item in self.testData:
			user = self.user_to_id[str(item[0])]
			movie = item[1]
			rui = float(item[2])
			rui2 = self.avgRate + self.bu[user] + self.bi[self.movieData[movie]['id']]+numpy.matmul(self.p[user],self.q[:,self.movieData[movie]['id']])
			rl = [rui,rui2]
			ruilist.append(rl)
			e = float(rui) - float(rui2)
			rmse += e * e
			rmseNum += 1
		self.compareData = numpy.array(ruilist)
		

		rmse = ((rmse/rmseNum)**0.5)
		self.testRmse = rmse
		print  '---------------- Test RMSE = %f -------------------------'% float(rmse)

	def printData(self):
		print '--over ndim = %d,alpha = %f,lamba = %f ,times = %d,trainRmse = %f,testRmse = %f--------' %(self.ndim ,self.alpha,self.lamba,self.circleTime,self.trainRmse,self.testRmse)

	def saveData(self):
		localtime = time.localtime(time.time())
		#save compare
		c = DataFrame(self.compareData)
		c.to_csv('../svd/save/compare.csv',index=False,header =False)
		print '--------------File compare saved -----------------'
		#save p 
		c = DataFrame(self.p)
		c.to_csv('../svd/save/p.csv',index=False,header =False)
		print '--------------File p saved -----------------'
		#save q 
		c = DataFrame(self.q)
		c.to_csv('../svd/save/q.csv',index=False,header =False)
		print '--------------File q saved -----------------'
		#save bu 
		c = DataFrame(self.bu)
		c.to_csv('../svd/save/bu.csv',index=False,header =False)
		print '--------------File bu saved -----------------'
		#save bi 
		c = DataFrame(self.bi)
		c.to_csv('../svd/save/bi.csv',index=False,header =False)
		print '--------------File bi saved -----------------'
		#save id_to_movie 
		# c = DataFrame(self.id_to_movie)
		# c.to_csv('save/id-to-movie.csv',index=False,header =False)
		# print '--------------File id_to_movie saved -----------------'
		#save avgRate 
		file  = open('../svd/save/avg.txt','w+')
		file.write(str(self.avgRate))
		file.close()
		print '--------------File avgRate saved -----------------'
		#save r
		# header = []
		# for item in self.id_to_movie:
		# 	header.append( self.id_to_movie[item]['title'])
		# r = numpy.matmul(self.p,self.q)
		# c = DataFrame(r)
		# c.to_csv('save/r.csv',index=False,header =header)
		# print '--------------File r saved -----------------'

