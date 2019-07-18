# This script contains the main calculation functions for GPSmain.py

import numpy as np
from termcolor import colored

import GPSfns


#function to calculate pseudoranges from approximate station position (rApprox) to satellite  
def calcs(satNum, coordinates, ranges, rApprox):

	#define constants and read in given values needed

#speed of light (m/s)
	c = 299792458
#earth rotation rate (rad/s)
	wEarth = 7.292115e-5
#satNum used as index for input and output arrays 
	i = satNum 
#given values 
	rECEFepoch = np.array(coordinates[ i, 0, : ])	#r_i(t)
	bias = ranges[ i, 0]				#tao_i
	oPseudo = ranges[ i, 1]				#o_i
	vECEFsat = np.array(coordinates[ i, 1, : ])	#v_i

###	print('\n\nVariables done for Satellite {} *************\n\n' .format(i))

	print('\n\n\n\t************ Computations for Satellite', i, '************\n\n')

# Computation Section ----------------

#ECI = ECEF at time signal recieved so no need to transform rApprox here
#epoch not yet adjusted for reciever bias yet because tau unknown (found in least squares)
#need approx station coordinates, sat clock bias, sat position and velocity to start calcs


	#epoch range vector (meters - 3D value)

#initial range vector estimate, assume no satellite or station velocity
	rTrans1 = rApprox - rECEFepoch
#check if values match given results
	checkTuple = GPSfns.coordsCheck(rTrans1, i, 2, .01, coordinates)
	if checkTuple[0]:
		print(' Initial epoch range vector:  \t({:.3f}, {:.3f}, {:.3f}) meters' .format(checkTuple[2][0], checkTuple[2][1], checkTuple[2][2]))
		print(' Matches given value to {:.1f} %\n' .format(checkTuple[1] * 100))
	else:
		print('\n\n{}\n\n' .format(colored('ERROR', 'red')))

	#epoch range (m - linear value)

#range is absolute value of epoch vector
	transR1 = np.sqrt(rTrans1[0] ** 2 + rTrans1[1] ** 2 +rTrans1[2] ** 2) 
#check if values match given results
	checkTuple = GPSfns.rangeCheck(transR1, i, 2, .01, ranges)
	if checkTuple[0]:
		print(' Initial epoch range:  \t\t{:.3f} meters' .format(checkTuple[2]))
		print(' Matches given value to {:.1f}%\n' .format(checkTuple[1] * 100))
	else:
		print('{} of {} %  ({} vs {})' .format(colored('ERROR', 'red'), checkTuple[3], checkTuple[2], ranges[i, 2]))
#for i in range(0, iterateT)-------------iterate here if wanted

	#flight time (seconds - linear)

#initial fly time estimate using range estimate
#this estimate is good because range estimate off by ~ 80m but light takes << fly time to travel this distance
	fly = transR1 / c
#check time with given results
	checkTuple = GPSfns.rangeCheck(fly, i, 3, .01, ranges)
	if checkTuple[0]:
		print(' Initial time of flight:  \t{:.3f} seconds' .format(checkTuple[2]))
		print(' Matches given value to {:.1f} %\n' .format(checkTuple[1] * 100))
	else:
		print('{} of {} %  ({} vs {})' .format(colored('ERROR', 'red'), checkTuple[3], checkTuple[2], ranges[i, 3]))

	#earth centered, earth fixed (ECEF) transmit position (m - 3D)

#linearly extrapolate satellite position back to transmit time in ECEF
	rECEFtrans = rECEFepoch - vECEFsat * fly
#check if values match given results
	checkTuple = GPSfns.coordsCheck(rECEFtrans, i, 3, .01, coordinates)
	if checkTuple[0]:
		print(' ECEF transmit position:  \t({:.3f}, {:.3f}, {:.3f}) meters' .format(checkTuple[2][0], checkTuple[2][1], checkTuple[2][2]))
		print(' Matches given value to {:.1f} %\n' .format(checkTuple[1] * 100))
	else:
		print('{}' .format(colored('ERROR', 'red')))


	#earth centered, inertial (ECI) transmit positon (m - 3D)
	
#matrix to transform ECEF transmit position to ECI (now the satellite directly above TONO at transmit time) 
	rotationMatrix = GPSfns.rot(wEarth * fly, 3, False)
#apply matrix on ECEF position
	rECItrans = np.dot(rotationMatrix, rECEFtrans)
#check if values match given results
	checkTuple = GPSfns.coordsCheck(rECItrans, i, 4, .01, coordinates)
	if checkTuple[0]:
		print(' ECI transmit position:  \t({:.3f}, {:.3f}, {:.3f}) meters' .format(checkTuple[2][0], checkTuple[2][1], checkTuple[2][2]))
		print(' Matches given value to {:.1f} %\n' .format(checkTuple[1] * 100))
	else:
		print('\n\n{}\n\n' .format(colored('ERROR', 'red')))


	#transmit range vector from satellite transmit position to station receive position (m - 3D)

#revised range vector from TONO to satellite transmit position directly above (first estimated: rApprox - rECEFepoch)
	rTrans = rApprox - rECItrans
#check if values match given results
	checkTuple = GPSfns.coordsCheck(rTrans, i, 5, .01, coordinates)
	if checkTuple[0]:
		print(' Revised (transmit) range vector:  \t({:.3f}, {:.3f}, {:.3f}) meters' .format(checkTuple[2][0], checkTuple[2][1], checkTuple[2][2]))
		print(' Matches given value to {:.1f} %\n' .format(checkTuple[1] * 100))
	else:
		print('\n\n{}\n\n' .format(colored('ERROR', 'red')))


	#transmit range (m - linear)

#absolute value for revised transmit range 
	transR = np.sqrt(rTrans[0] ** 2 + rTrans[1] ** 2 + rTrans[2] ** 2) 
#check coordinates with given results
	checkTuple = GPSfns.rangeCheck(transR, i, 4 , .01, ranges)
	if checkTuple[0]:
		print(' Revised (transmit) range:  \t{:.3f} seconds' .format(checkTuple[2]))
		print(' Matches given value to {:.1f} %\n' .format(checkTuple[1] * 100))
	else:
		print('{} of {} %  ({} vs {})' .format(colored('ERROR', 'red'), checkTuple[3], checkTuple[2], ranges[i, 4]))

## ---------
#for iterative fly time calculation take fly = transR / c and repeat steps: flight time to here 


#ECI method -----------------
	#earth centered, inertial (ECI) transmit positon (m - 3D)
#how to add earths rotation???????????
#vsatECI = coordinates[ i, 1, : ] + [wEarth, 0, 0]
#start loop for iteration here (newFlyT -> flyT)
#transform ECEF to ECI
#####rECItrans = rECIepoch - (vsatECI * fly)
	#transmit range vector from satellite transmit position to station receive position (m - 3D)
#####rFlyT = (rTONOepoch - rECItrans)
#####trans = epoch - x
	#transmit range (m - linear)
#more accurate range estimate than used for fly time estimate
#iterate by using more accurate range (unecessary for orbit distances around earth)
#####newFlyT = transR / c
#----------------------

	#computed pseudorange (subtract satellite clock bias from range) (m - linear)

	cPseudo = transR - bias
#check coordinates with given results
	checkTuple = GPSfns.rangeCheck(cPseudo, i, 5 , .01, ranges)
	if checkTuple[0]:
		print(' Computed pseudorange:  \t{:.3f} seconds' .format(checkTuple[2]))
		print(' Matches given value to {:.1f} %\n' .format(checkTuple[1] * 100))
	else:
		print('{} of {} %  ({} vs {})' .format(colored('ERROR', 'red'), checkTuple[3], checkTuple[2], ranges[i, 5]))


	#observed - computed
	
	oc = oPseudo - cPseudo
#check coordinates with given results
	checkTuple = GPSfns.rangeCheck(oc, i, 6 , .03, ranges)
	if checkTuple[0]:
		print(' Observed - computed value:  \t{:.3f} seconds' .format(checkTuple[2]))
		print(' Matches given value to {:.1f} %\n' .format(checkTuple[1] * 100))
	else:
		print('{} of {} %  ({} vs {})' .format(colored('ERROR', 'red'), checkTuple[3], checkTuple[2], ranges[i, 6]))


# Summarization Section -----------------

#read values into computed data set for visual comparison
	cCoords_i = np.array([[rTrans1],[rECEFtrans],[rECItrans],[rTrans]])
#resize because above results in shape of (4,1,3)
	cCoords_i.resize(4,3)
	
#do same for ranges
	cRanges_i = np.array([[transR1],[fly],[transR],[cPseudo],[oc]])
	cRanges_i.resize(5)


	#####
	#Compute partials for use in least squares
	#

#functional model is c(flytime) + station bia - sat bias
#	or c_i = transR +,- biases (typos in slides transR^2 ???????)
#		--> c_i = transR_o - sat bias
#		--> o_i - c_i, (oc) = o_i - transR_o + sat bias
#	Where o and c are pseudoranges

#Functional model is [rTrans_x,y,z/transR, right row = 1], each sat is row in partials matrix.
#	where transR_x,y,z are (x_o - xECItrans)

#1 in right row is from partial with respect to sat bias (bias has no powers, coefficients)
#All in vectors in ECI

#create empty array for partials (bias partial is 1 because it is has no coefficients or powers)
	partials = np.array([0.0, 0.0, 0.0, 1.0])
#compute partials for x, y, z parameters for sat# satNum
	for j in range (0, 3):
	#jth component of rECItrans
	#	print(cCoords_i[2, j])
	#transR
	#	print(cRanges_i[2])
	#approximate parameter j
	#	print(rApprox[j])

		partials[j] = ((rApprox[j] - cCoords_i[2, j])/cRanges_i[2])


	return(cCoords_i, cRanges_i, partials)

# END of pseudoCalc Function
