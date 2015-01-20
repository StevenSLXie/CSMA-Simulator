from Source import Source
from action import action
import operator
import random
from initialization import initialization
from particleFilter import generateParticles, run
import csv
from ARMA import ARMAFilter, transfer
from EKF import kalman_update
import numpy as np
import os


def runSimulation(number):
	numOfNodes = number+1

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
		t = random.randint(20, 150)*20
		e = initialization(t, i, numOfNodes)
		eventList.append(e)

	min_t = 0

	flag = True
	timer = 20
	data = []
	while True:
		if not eventList:
			break
		elif min_t > fromSecondToSlot(5):  # 6250000  # *4/250000
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
				temp.append(nodes[i].getChannelIndicators(450, 160))

			data.append(temp)
			# and set the condition
			timer += 10

	writer = csv.writer(open('data3.csv', 'w'))

	for eachData in data:
		writer.writerow([eachData[0][0], 1.0-eachData[0][1]])
	return


def fromSecondToSlot(second):
	return second*250000/4


def fromSlotToSecond(slot):
	return slot*4/250000


def runParticeFiltering():

	os.chdir('..')

	particles = generateParticles()

	writer = csv.writer(open('data/new_traffic/est-PF-0.5-2000.csv', 'w'))

	with open('src/data3.csv', 'rb') as file:
		data = csv.reader(file, delimiter=',')
		for d in data:
			particles, estTP, estU= run(float(d[0]), float(d[1]), particles)
			writer.writerow([estTP, estU])
			print estTP, estU
	return


def runARMAFiltering():

	os.chdir('..')


	beta = 0
	psr = 0

	writer = csv.writer(open('data/estimation-0.csv', 'w'))


	with open('src/data2.csv', 'rb') as file:
		data = csv.reader(file, delimiter=',')
		for d in data:
			beta, psr, estTP, estU = ARMAFilter(float(d[0]), float(d[1]), beta, psr)
			writer.writerow([estTP, estU])
			# print float(d[0]), float(d[1]), transfer(float(d[0]), float(d[1]))
			print estTP, estU


def runKalmanFiltering():

	os.chdir('..')

	writer = csv.writer(open('data/est-ARMA.csv', 'w'))

	np_P = np.array([[100, 0], [0, 100.0]])
	transProb = 0.01
	usage = 0.5

	with open('src/data2.csv', 'rb') as file:
		data = csv.reader(file, delimiter=',')
		for d in data:
			transProb, usage, np_P = kalman_update(float(d[0]), float(d[1]), transProb, usage, np_P)
			writer.writerow([transProb, usage])
			print transProb, usage



runSimulation(22)
#runParticeFiltering()
# runKalmanFiltering()
# runARMAFiltering()

