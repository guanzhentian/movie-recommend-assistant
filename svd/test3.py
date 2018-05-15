from svd import svd
import time
starttime = time.time()

alpha = 0.003
lamba = 0.01

svd2 = svd(3,  alpha, lamba,10)
svd2.printData()
svd2.saveData()


endtime = time.time()
print '\n-----------csv data load finished ,cost time %f -------------\n'% (endtime - starttime)