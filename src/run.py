from Source import Source
from action import action
import operator
import random
from initialization import initialization


def runSimulation(number):
	numOfNodes = number

	nodes = []

	for i in range(numOfNodes):  # initialize nodes
		argv = {}
		argv['ID'] = i
		argv['src'] = i
		argv['des'] = numOfNodes - 1
		n = Source(argv)
		nodes.append(n)

	eventList = []
	#for i in range(numOfNodes-1):
	#	nodes[i].setPacInterval(dataRate)

	for i in range(numOfNodes-1):
		t = random.randint(1800,4200)
		e = initialization(t,i,numOfNodes)
		eventList.append(e)

	min_t  = 0

	time = []
	while True:
		if not eventList:
			break
		elif min_t > fromSecondToSlot(100):  # 6250000  # *4/250000
			break
		else:
			min_index, min_t = min(enumerate(e.time for e in eventList),key=operator.itemgetter(1))
			newList = action(eventList[min_index],nodes,'normal')
			eventList.pop(min_index)
			for n in newList:
				eventList.append(n)
			#print min_t, min_index, 'try'
	return

def fromSecondToSlot(second):
	return second*250000/4

runSimulation(82)
