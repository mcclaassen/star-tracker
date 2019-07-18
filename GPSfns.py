# This file contains functions to be used in GPScalcs.py


import os
import math
import numpy as np
from termcolor import colored




# This function takes in 'value' and compares it to 'array' index [i][whichRange] to within 'tolerance'
#	In then prints a statement as to whether they matched to within relative (%) 'tolerance'
def rangeCheck(value, i, whichRange, tolerance, array):

		#check if values match given results to within the tolerance
	#bool for matching
	x = False
	#calculate % error
	error = (abs(value - array[i, whichRange]) * 100) / abs(array[i, whichRange])
	if np.isclose(value, array[i, whichRange], rtol = tolerance):
#		print(' Range {} matches for sat {} to {} %'.format(whichRange, i, error))
		x = True
#	else:
#		print(' Range {} has {} % {} for sat {}'.format(whichRange, error, colored('ERROR', 'red'), i)) 

	return (x, tolerance, value, error)

# This function takes in 'value' (an array here) and compares it to 'array[i][whichCoords][ : ]'
#	In then prints a statement as to whether they matched to within 'tolerance'
def coordsCheck(value, i, whichCoords, tolerance, array):

		#check if values match given results
	#bool for matching
	x = False
	
	#calculate % error
	error =	(abs(value - array[i, whichCoords]) * 100) / array[i, whichCoords]
	#create boolean array for match with whole coords array (can be optimized for just relevant row??????????)
	boolArray = np.isclose(value, array, rtol = tolerance)
	#check if all values in relevant row match caculated values
	if np.all(boolArray[i, whichCoords]):
#		print(' Vector {} matches for sat {} to {} %'.format(whichCoords, i, error)) 
		x = True
#	else:
#		print(' Vector {} has {} % {} for sat {}'.format(whichCoords, error, colored('ERROR', 'red'), i)) 

	return (x, tolerance, value, error)


# This function takes in 'theta' and returns one of three rotation matrices with theta as the rotation angle
#	If theta is very small, 'infinitessimal' can be set to True, causing sin ->'theta' and cos -> 1
def rot(theta, matrixNumber, BOOLinfinitessimal):
	
	if BOOLinfinitessimal == False:
		c = np.cos(theta)
		s = np.sin(theta)
	elif BOOLinfinitessimal == True:
		c = 1
		s = theta
	else:
		print('{} rotation argument' .format(colored('Incorrect', 'red')))
	if matrixNumber == 1:
		R = np.array([[ 1, 0 , 0],[ 0, c, s],[ 0, -s, c]])
	elif matrixNumber == 2:
		R = np.array([[ c, 0 , -s],[ 0, 1, 0],[ s, 0, c]])
	elif matrixNumber == 3:
		R = np.array([[ c, s , 0],[ -s, c, 0],[ 0, 0, 1]])
	else:
		print('{} rotation argument' .format(colored('Incorrect', 'red')))

	return R
