from Source import Source
from action import action
import operator
import random
from initialization import initialization
from particleFilter import generateParticles, run
import csv


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
		t = random.randint(20,150)*20
		e = initialization(t,i,numOfNodes)
		eventList.append(e)

	min_t = 0

	flag = True
	timer = 10
	data = []
	while True:
		if not eventList:
			break
		elif min_t > fromSecondToSlot(50):  # 6250000  # *4/250000
			break
		else:
			min_index, min_t = min(enumerate(e.time for e in eventList),key=operator.itemgetter(1))
			newList = action(eventList[min_index], nodes, 'normal')
			eventList.pop(min_index)
			for n in newList:
				eventList.append(n)

		if min_t > fromSecondToSlot(timer):
			# perform the collection
			temp = []
			for i in range(numOfNodes-1):
				temp.append(nodes[i].getChannelIndicators(200))

			data.append(temp)
			# and set the condition
			timer += 1


	particles = generateParticles()

	writer = csv.writer(open('data.csv', 'w'))

	for eachData in data:
		particles, estTP, estU = run(eachData[0][0], 1-eachData[0][1], particles)
		print eachData[0][0], eachData[0][1]
		# for p in particles:
		#	 print p.transProb, p.usage, p.weight
		print estTP, estU
		writer.writerow([estTP, estU])

	return


def fromSecondToSlot(second):
	return second*250000/4


def fromSlotToSecond(slot):
	return slot*4/250000

runSimulation(31+1)

