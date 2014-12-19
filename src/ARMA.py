import math as mt

smooth = 0

def ARMAFilter(betaNew, psrNew, betaOld=0, psrOld=0):

	if betaOld == 0 and psrOld == 0:
		betaOld = betaNew
		psrOld = psrNew

	beta = betaNew * (1-smooth) + smooth * betaOld
	psr =  psrNew * (1-smooth) + smooth * psrOld
	transProb, usage = transfer(beta, psr)

	return beta, psr, transProb, usage


def transfer(beta, psr):
	m = 4
	n = 20

	prod = psr/(1-beta**(m+1))
	c = (1-beta**(m+1))/(1-beta)
	transProb = n/c * (1-mt.exp(mt.log(prod)/n))
	usage = ((1/(1-beta)-1)/(1-prod)-1)*transProb

	return transProb, usage

