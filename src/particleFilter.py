# -*- coding: utf-8 -*-
"""

Acknowledgement: This file is based on the code in https://sites.google.com/site/ericzhangxiuming/tut/pf. The author is Xiuming Zhang.

"""

import numpy as np
import math as mt
import random as rdm
from numpy import linalg as li

PARTICLE_NO = 3000
# estimated measurement uncertainty
HD_UNCERTAINTY_MEAN = 0
HD_UNCERTAINTY_SIGMA = 0.1
SL_UNCERTAINTY_MEAN = 0
SL_UNCERTAINTY_SIGMA = 0.5

class Particle(object):
	# constructor
	def __init__(self, transProb=None, usage=None, weight1= 1.0/PARTICLE_NO, weight2 = 1.0/PARTICLE_NO):
	# transProb is the aggregate transmission probability of all other nodes;
	# usage is the aggregate channel usage of all other nodes;
		self.transProb = transProb
		self.usage = usage
		self.weight1 = weight1
		self.weight2 = weight2


def run(beta, psr, particles):

	## update all the particles
	for k in xrange(len(particles)):
		### PREDICT
		# particles[k] = _move(particles[k])
		### MEASURE
		particles[k] = _weighting(particles[k], beta, psr)
	### NORMALIZE
	particles = _normalize(particles)
	### RESAMPLE
	# particles = _resample(particles)
	# for p in particles:
	#	print p.weight
	estTransProb, estUsage = _avgParticleWOResample(particles)

	return particles, estTransProb, estUsage


def generateParticles():
	particles = []
	while np.size(particles) < PARTICLE_NO:
		t = _getRandomTransProb()
		u = _getRandomUsage(t)
		if _feasibility(t, u) != 0:
			p = Particle(t, u) # construct a particle object
			particles.append(p)
	return particles


def _getRandomTransProb():
	transProb = rdm.random()*0.2
	return transProb

def _getRandomUsage(transProb):
	usage = rdm.uniform(4, 8)*transProb
	return usage

def _getCom():
	return rdm.random()*0.8

def _feasibility(transProb, usage):
	if transProb<1 and usage < 1:
		return 1
	else:
		return 0

def _move(p):
	newP = Particle()

	newP.transProb = p.transProb + rdm.uniform(-0.0001, 0.0001)
	newP.usage = p.usage + rdm.uniform(-0.003, 0.003)
	newP.weight1 = p.weight1
	newP.weight2 = p.weight2

	return newP

def _weighting(p, beta, psr):
	t1, t2= _transfer(beta, psr)
	m = 4

	B  = 400
	D  = 160
	cov = [[beta*(1-beta)/B, beta**(m+1)*(1-beta)/B],[beta**(m+1)*(1-beta)/B, psr*(1-psr)/D]]
	np_cov = np.array(cov)
	np_cov_inv = li.inv(np_cov)
	x = np.array([p.transProb-t1, p.usage-t2])

	temp = max(0, np.dot(np.dot(x,np_cov_inv), x.transpose()))

	# print temp

	weight1 = mt.exp(-0.5*temp)

	weight2 = 0.1

	# weight1 = mt.exp(-(100*(p.transProb-t1)+100*(p.usage-t2))**2)
	# weight2 = mt.exp(-(50*(p.usage-t2))**2)

	# print weight1

	# p.weight  = 0.8*weight + 0.2*p.weight
	# p.weight1 = 0.005*weight1 + 0.995*p.weight1
	# p.weight2 = 0.005*weight2 + 0.995*p.weight2
	# p.weight3 = 0.005*weight3 + 0.995*p.weight3
	p.weight1 *= weight1
	p.weight2 *= weight2
	# print p.weight1, p.weight2, p.transProb, p.usage
	return p

def _transfer(beta, psr):
	m = 4
	n = 20
	# from (beta,psr) to (transProb,usage)
	# transProb = (1-psr/(1-beta**(m+1)))*(1-beta)/(1-beta**(m+1))
	# usage = 1/(1-beta**(m+1))*(2*beta-1+(1-beta)*psr/(1-beta**(m+1)))
	# usage = beta/(1-beta**(m+1))-transProb

	prod = psr/(1-beta**(m+1))
	c = (1-beta**(m+1))/(1-beta)
	transProb = n/c * (1-mt.exp(mt.log(prod)/n))
	usage = ((1/(1-beta)-1)/(1-prod)-1)*transProb

	return transProb, usage

## optional normalization
def _normalize(particles):
	N = len(particles)
	weightSum = [0, 0, 0]
	for p in particles:
		weightSum[0] += p.weight1
		weightSum[1] += p.weight2


	for p in particles:
		p.weight1 = 1.0*p.weight1/weightSum[0]
		p.weight2 = 1.0*p.weight2/weightSum[1]
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


def _avgParticleWOResample(particles):

	transProbSum = 0
	usageSum = 0

	for p in particles:
		transProbSum += (p.transProb*p.weight1)
		usageSum += (p.usage*p.weight1)
	return transProbSum, usageSum


def _avgParticleWResample(particles):
	transProbSum = 0
	usageSum = 0

	for p in particles:
		transProbSum += p.transProb
		usageSum += p.usage

	transProbSum /= PARTICLE_NO
	usageSum /= PARTICLE_NO
	return transProbSum, usageSum



