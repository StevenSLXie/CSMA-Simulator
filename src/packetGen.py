import numpy
import random

def pacGenerator(poiInterval,numPac,offsetEnd,offsetStart=0):
	seq = numpy.random.poisson(poiInterval,numPac)
	timeSum = random.randint(offsetStart,offsetEnd)
	time = []
	for i in range(len(seq)):
		timeSum = timeSum + seq[i]
		time.append(timeSum)
#print time
	return time


