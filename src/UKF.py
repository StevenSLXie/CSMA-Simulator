'''
==============================================
Using the Unscented Kalman Filter and Smoother
==============================================
This simple example shows how one may apply the Unscented Kalman Filter and
Unscented Kalman Smoother to some randomly generated data.
The Unscented Kalman Filter (UKF) and Rauch-Rung-Striebel type Unscented Kalman
Smoother (UKS) are a generalization of the traditional Kalman Filter and
Smoother to models with non-linear equations describing state transitions and
observation emissions. Unlike the Extended Kalman Filter (EKF), which attempts
to perform the same task by using the numerical derivative of the appropriate
equations, the UKF selects a handful of "sigma points", passes them through the
appropriate function, then finally re-estimates a normal distribution around
those propagated points. Experiments have shown that the UKF and UKS are
superior to the EKF and EKS in nearly all scenarios.
The figure drawn shows the true, hidden state; the state estimates given by the
UKF; and finally the same given by the UKS.
'''


import numpy as np
import pylab as pl
from pykalman import UnscentedKalmanFilter
import csv



transition_covariance = np.eye(2)*0.001
random_state = np.random.RandomState(0)
observation_covariance = np.eye(2)*0.001 + random_state.randn(2, 2) * 0.1
initial_state_mean = [0.05, 0.3]
initial_state_covariance = [[1, 0.1], [-0.1, 1]]

def transition_function(state, noise):
	C = np.eye(2) + noise
	return np.dot(C, state)


def observation_function(state, noise):
	a = state[0]+state[1] + noise[0]
	b = 1 - state[0]/(1-state[0]-state[1]) + noise[1]
	return np.array([a, b])

def main():
	# sample from model
	kf = UnscentedKalmanFilter(
		transition_function, observation_function,
		 observation_covariance,

	)

	# states, observations = kf.sample(50, initial_state_mean)

	observations = []

	import os
	dir = os.path.dirname(os.path.realpath(__file__))

	with open(dir+'/data.csv', 'rb') as csvfile:
		para = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in para:
			observations.append(row)

	states = []
	cov = []
	for i in range(len(observations)):
		states.append([0, 0])
		cov.append([[0, 0], [0, 0]])
	states[0] = initial_state_mean
	print states[0]
	cov[0] = initial_state_covariance
	for i in range(len(observations)-1):
		states[i], cov[i] = kf.filter(observations[i+1])
		states[i+1], cov[i+1] = kf.filter_update(states[i], cov[i])


	# estimate state with filtering and smoothing
	# filtered_state_estimates = kf.filter(observations)[0]
	# smoothed_state_estimates = kf.smooth(observations)[0]

	# draw estimates
	pl.figure()
	lines_true = pl.plot(states, color='b')
	# lines_filt = pl.plot(filtered_state_estimates, color='r', ls='-')
	# lines_smooth = pl.plot(smoothed_state_estimates, color='g', ls='-.')
	#pl.legend((lines_true[0], lines_filt[0], lines_smooth[0]),
	#		  ('true', 'filt', 'smooth'),
	#		  loc='lower left'
	#)
	pl.show()

