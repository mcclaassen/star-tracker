# This function uses least squares inversion to turn a GPS pseudorange into a more precise position estimate

import numpy as np
import sympy as sp
from sympy.abc import x,y,z

import GPSfns


def partials(satNum, ranges, vectors, checkPartials, rApprox):
	rTONO = [-2296700.0, -4472150.0, 3915300.0]

#declare symbolic array of initial parameters (x_o), bias initial parameter = 0
#	this is a numpy array so that it may be in an equation with ranges, vectors
	initialParameters = np.array([x, y, z])

#functional model is c(flytime) + station bia - sat bias
#	or c_i = transR +,- biases (typos in slides transR^2 ???????)

#approx parameters = x_o, y_o, z_o, and 0 for station bias (drift linear so may take initial anywhere)

#--> c_i = transR_o - sat bias
#--> o_i - c_i, (oc) = o_i - transR_o + sat bias
#	where o and c are pseudoranges

#partial of functional model are d/(d parameter)*[(rTrans_x^2 + rTrans_y^2 + rTrans_z^2)]^1/2 - sat bias]
# 	or [rTrans_x,y,z/transR, right row = 1] where each satellite is a row in partials matrix.
#	1 at right is from partial with respect to sat bias
#	all in ECI

#transR_x,y,z are (x_o - xECItrans)
	
	partialsEq = sp.Matrix([[0, 0, 0, 1]])

#compute partials for x, y, z parameters for sat# satNum
	for i in range (0,3):
	#rECItrans_x,y,z component
		print(vectors[satNum, 2, i])
	#transR for sat: satNum
		print(ranges[satNum, 2])
#symbolic expression of partial with respect to each of i coordinates
		partialsEq[i] = sp.exp((initialParameters[i] - vectors[satNum, 2, i])/ranges[satNum, 2])
	print(partialsEq)
#check if cPartials match given values
#	GPSfns.coordsCheck(partials, satNum, 0, .01, checkPartials)
	print(rTONO)
	partialsEq.subs({x:rTONO[0], y:rTONO[1], z:rTONO[2]})
	print(partialsEq)
	return partials
