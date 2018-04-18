from svd import svd

alpha = 0.003
lamba = 0.01

svd2 = svd(1,  alpha, lamba,20)


svd2.printData()
name = svd2.saveData()
print name