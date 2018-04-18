import csv
import numpy
import time
from pandas import DataFrame
import os 

class svd(object):
	"""docstring for svd 0.005 0.02"""
	def __init__(self, ndim ,alpha ,lamba ,times ):
		self.basicDataDir = 'ml-latest-small'
		dataname = self.basicDataDir+'/ratings.csv'
		y = self.handleCsvData(dataname,True)  
		
		self.ndim = ndim 		
		self.test_proportion = 0.2
		self.user_rate_data = y

		self.martix = numpy.array(y,dtype = numpy.float64) 
		maxdata = self.martix.max(axis = 0)
		self.user = int(maxdata[0]) 	

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

		self.handleMovieData()
		self.initData()
		self.train()
		self.test()

		

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
		return allRow	

	def  handleMovieData(self):
		starttime = time.time()
		link = self.basicDataDir+'/movies.csv'
		reader = csv.reader(file(link))
		reader.next()
		md = {}
		itm = {}
		num = 0
		for row in reader:
			newData = {
				'title':row[1],
				'genres':row[2],
				'id':num
			}
			newData2 = {
				'title':row[1],
				'genres':row[2],
				'movieId':row[0]
			}
			md[row[0]] = newData
			itm[num] = newData2
			num+=1

		self.id_to_movie = itm
		self.movie =len(md)
		self.movieData =  md
		endtime = time.time()
		print '-----------movie data load finished,cost time %f   -----------------\n'% (endtime - starttime)

	def initData(self):
		starttime = time.time()

		#get train data & test data
		numPop = int(0.2*len(self.user_rate_data))
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
				# rd = numpy.random.uniform(0,0.5)
				rd = 0
				row.append(rd)
			userArray.append(row)

		self.p = numpy.array(userArray,dtype = numpy.float64)

		#init q
		itemArray = []
		for i in range(0,self.ndim):
			row = []
			for j in range(0,self.movie):
				# rd = numpy.random.uniform(0,0.5)
				rd = 0
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
				user = int(item[0]) - 1 
				movie = item[1]
				rui = float(item[2])
				rui2 = self.avgRate + self.bu[user] + self.bi[self.movieData[movie]['id']] + numpy.matmul(self.p[user],self.q[:,self.movieData[movie]['id']])				
				# if rui2 > 5:
				# 	rui2  = 5
				# elif rui2 < 0:
				# 	rui2 = 0
				e = float(rui) - float(rui2)

				#train
				self.bu[user] += self.alpha*(e - self.lamba * self.bu[user])
				self.bi[self.movieData[movie]['id']] += self.alpha*(e - self.lamba * self.bi[self.movieData[movie]['id']])
				for i in range(0,self.ndim):
					self.p[user,i] += self.alpha*(e*self.q[i,self.movieData[movie]['id']] - self.lamba * self.p[user,i])
					self.q[i,self.movieData[movie]['id']] += self.alpha*(e*self.p[user,i] - self.lamba * self.q[i,self.movieData[movie]['id']])
				rmse += e * e
				rmseNum += 1
			# self.alpha *= 0.9
			# print (rmse,rmseNum)
			rmse = ((rmse/rmseNum)**0.5)

			try:
				print  '----------------%d Train RMSE = %f -------------------------'% (k,float(rmse))
			except:
				print("Unexpected error")

			if rmse > lastRmse:
				print '----------------%d Train RMSE up-------------------------' % k
				break
			else:
				lastRmse = rmse
		self.trainRmse = rmse	
		endtime = time.time()
		print '-----------initData finished,cost time %f   -----------------\n'% (endtime - starttime)

	def test(self):
		starttime = time.time()
		rmse = 0
		rmseNum = 0
		ruilist = []
		for item in self.testData:
			user = int(item[0]) - 1 
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
		name = str(localtime.tm_mon)+'-'+str(localtime.tm_mday)+' '+str(localtime.tm_hour)+'-'+str(localtime.tm_min)+'-'+str(localtime.tm_sec)
		os.mkdir('save/'+name)
		#save compare
		c = DataFrame(self.compareData)
		c.to_csv('save/'+name+'/compare.csv',index=False,header =False)
		print '--------------File compare saved -----------------'
		#save p 
		c = DataFrame(self.p)
		c.to_csv('save/'+name+'/p.csv',index=False,header =False)
		print '--------------File p saved -----------------'
		#save q 
		c = DataFrame(self.q)
		c.to_csv('save/'+name+'/q.csv',index=False,header =False)
		print '--------------File q saved -----------------'
		#save r
		header = []
		for item in self.id_to_movie:
			header.append( self.id_to_movie[item]['title'])
		r = numpy.matmul(self.p,self.q)
		c = DataFrame(r)
		c.to_csv('save/'+name+'/r.csv',index=False,header =header)
		print '--------------File r saved -----------------'

		return 'save/'+name

