import numpy as np

m = 4
B = 400
D = 160

np_Q = np.array([[0.00, 0.0], [0.0, 0.00]])

def kalman_update(beta, psr, transProbOld, usageOld, np_P):
	# this update function takes in a new set of (beta, psr) and returns the current prediction of (transProb, usage)
	temp_beta, temp_psr = _inv_transfer(transProbOld, usageOld)

	z = np.array([beta-temp_beta, psr-temp_psr]).transpose()

	# print temp_beta, temp_psr, z

	np_P += np_Q

	# R = [[beta*(1-beta)/B, beta**(m+1)*(1-beta)/B], [beta**(m+1)*(1-beta)/B, psr*(1-psr)/D]]
	R = [[beta*(1-beta)/B, 0], [0, psr*(1-psr)/D]]

	np_R = np.array(R)

	np_hk = _dif_inv_transfer(transProbOld, usageOld)

	# print np_hk

	np_S = np.dot(np.dot(np_hk, np_P), np_hk.transpose()) + np_R

	np_K = np.dot(np.dot(np_P, np_hk.transpose()), np.linalg.inv(np_S))

	x = np.array([transProbOld, usageOld]).transpose() + np.dot(np_K, z)

	np_P = np.dot(np.eye(2)-np.dot(np_K, np_hk), np_P)

	return x[0], x[1], np_P


def _dif_inv_transfer(transProb, usage):
	delta = 0.001
	beta0, psr0 = _inv_transfer(transProb, usage)

	beta1, psr1 = _inv_transfer(transProb+delta, usage)
	beta2, psr2 = _inv_transfer(transProb, usage+delta)

	delta_h = np.array([[(beta1-beta0)/delta, (beta2-beta0)/delta], [(psr1-psr0)/delta, (psr2-psr0)/delta]])

	return delta_h


def _inv_transfer(transProb, usage):
	# checked
	n = 20
	lamb = transProb/float(n)

	dif = 10000
	can = 0

	for i in range(1, 800):
		beta = 0.001*i
		c = (1-beta**(m+1))/(1-beta)
		prod = (1-c*lamb)**n
		beta2 = 1-1.0/(1+(1-prod)*(1+usage/transProb))
		if abs(beta-beta2) < dif:
			dif = abs(beta-beta2)
			can = beta
			if dif < 0.0001:
				break

	beta = can
	c = (1-beta**(m+1))/(1-beta)
	prod = (1-c*lamb)**n

	psr = (1-beta**(m+1))*prod

	# print transProb, usage, beta, psr, lamb, prod

	return beta, psr



