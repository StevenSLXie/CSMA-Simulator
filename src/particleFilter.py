# -*- coding: utf-8 -*-
"""

Acknowledgement: This file is based on the code in https://sites.google.com/site/ericzhangxiuming/tut/pf. The author is Xiuming Zhang.

"""

import numpy as np
import math as mt
import random as rdm

PARTICLE_NO = 100
# estimated measurement uncertainty
HD_UNCERTAINTY_MEAN = 0
HD_UNCERTAINTY_SIGMA = 0.1
SL_UNCERTAINTY_MEAN = 0
SL_UNCERTAINTY_SIGMA = 0.5

class Particle(object):
	# constructor
	def __init__(self, transProb=None, usage=None, weight=0):
	# transProb is the aggregate transmission probability of all other nodes;
	# usage is the aggregate channel usage of all other nodes;
		self.transProb = transProb
		self.usage = usage
		self.weight = weight


def run(beta, psr, particles):

	## update all the particles
	for k in xrange(len(particles)):
		### PREDICT
		particles[k] = _move(particles[k])
		### MEASURE
		particles[k].weight = _weighting(particles[k],beta,psr)
	### NORMALIZE
	particles = _normalize(particles)
	### RESAMPLE
	particles = _resample(particles)
	estTransProb, estUsage = _avgParticle(particles)

	return particles, estTransProb, estUsage


def generateParticles():
	particles = []
	while np.size(particles) < PARTICLE_NO:
		t = _getRandomTransProb()
		u = _getRandomUsage(t)
		if _feasibility(t,u) != 0:
			p = Particle(t, u, 1.0) # construct a particle object
			particles.append(p)
	return particles


def _getRandomTransProb():
	transProb = rdm.random()*0.2
	return transProb

def _getRandomUsage(transProb):
	usage = rdm.randint(2,10)*transProb
	return usage

def _feasibility(transProb,usage):
	if transProb<1 and usage < 1:
		return 1
	else:
		return 0

def _move(p):
	newP = Particle()

	newP.transProb = p.transProb + np.random.normal(0,0.001)
	newP.usage = p.usage + np.random.normal(0.002)
	newP.weight = p.weight

	return newP

def _weighting(p,beta,psr):
	t1,t2 = _transfer(beta,psr)
	weight = mt.exp(-abs(mt.sqrt((p.transProb-t1)**2+(p.usage-t2)**2)))
	return weight


def _transfer(beta,psr):
	m = 4
	# from (beta,psr) to (transProb,usage)
	transProb = (1-psr/(1-beta**(m+1)))*(1-beta)/(1-beta**(m+1))
	usage = (1-beta**(m+1))*(2*beta-1+(1-beta)*psr/(1-beta**(m+1)))
	return transProb, usage

## optional normalization
def _normalize(particles):
	N = len(particles)
	weightSum = 0
	for p in particles:
		weightSum = weightSum + p.weight
	for i in xrange(N):
		particles[i].weight = 1.0 * particles[i].weight / weightSum
	return particles


def _resample(particles):
	resampledParticles = []
	beta = 0.0
	w = [e.weight for e in particles]
	mw = max(w)
	if mw != 0:
		index = int(np.random.random() * PARTICLE_NO)
		for k in xrange(PARTICLE_NO):
			beta += np.random.random() * 2.0 * mw # resampling wheel
			while beta > w[index]:
				beta -= w[index]
				index = (index + 1) % PARTICLE_NO
			resampledParticles.append(particles[index])
	else: # if all weights zero
		return particles
	return resampledParticles


def _avgParticle(particles):
	N = len(particles)
	transProbSum = 0
	usageSum = 0

	for p in particles:
		transProbSum += p.transProb
		usageSum += p.usage
	transProbSum = transProbSum / N
	usageSum = usageSum / N
	return (transProbSum, usageSum)


