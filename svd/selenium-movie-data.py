from pymongo import MongoClient
from selenium import webdriver
import time
import thread
from multiprocessing import Process
from multiprocessing import Pool

def getMes(val):
	print 'thred run in ',val
	browser = webdriver.Chrome()
	browser.get('http://localhost:3000/#/movie/'+val)
	time.sleep(8)
	browser.close()

if __name__=='__main__':
	client = MongoClient('mongodb://localhost:27017/')
	db = client.movie_recommend
	links = db.links
	data = links.find({})

	p = Pool()
	for i in range(0,links.count()):
		p.apply_async( getMes,args=(data[i]['tmdbId'],) )
	print 'Waiting for all subprocesses done...'
	p.close()
   	p.join()
   	print 'All subprocesses done.'
	



