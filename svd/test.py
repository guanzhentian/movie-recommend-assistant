import numpy
from pandas import DataFrame

a = [[1,2,3],[2,3,4]]
e = [[1,5,6],[2,5,6],[3,5,6]]
b = numpy.array(a,dtype = numpy.int32)
d = numpy.array(e,dtype = numpy.int32)

print b[1]
print d[:,1]
f = numpy.matmul(b[1],d[:,1])
print f
print f.shape