from Source import Source
from event import event


def initialization(t,src,n):
	argv = {}
	argv['time'] = t
	argv['actType'] = 'sendMac'
	argv['src'] = src
	argv['des'] = n - 1
	argv['pacSize'] = 60
	argv['pacData'] = src
	argv['pacType'] = 'data'
	argv['pacAckReq'] = True
	e = event(argv)
	return e

