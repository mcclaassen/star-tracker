#main GPS homework 2 script

import random
import numpy as np
from termcolor import colored

from GPSellipse import ellipse
from GPSfns import rot
from GPScorrection import rCorrection

		
	#######
	# Variable Reference Sheet --------------
	#

#epoch :	reciever time of signal reception (t)
#trans :	sat time of signal transmission (t_i')
#fly :		time of signal flight (delta t_i')		
## T
#adjEpoch :	

	#position vectors

#stationPosition : vector to station (r) (defined as ECI, ECEF equal when signal recieved)
#rECEFepoch :	sat vector when signal recieved by station in ECEF frame (r_i(t)) 	--given--
#rECIepoch :	sat vector when signal recieved by station in ECI frame (r_i(t))
#rECEFtrans :	sat vector when signal transmitted in ECEF frame (r_i(t_i'))
#rECItrans :	sat vector when signal transmitted in ECI frame (r_i(t_i'))
#rTrans :	sat vector when signal recieved by station (r_i(t))

	#ranges

#transR :	distance signal is transmitted (roe_i)
#bias :		sat clock bias (tao_i) 							--given--
#oPseudo :	observed pseudorange (o_i)						--given--
#cPseudo :	computed pseudorange (c_i)
#oc :		observed pseudorange minus computed pseudorange (o_i - c_i)  

	#satellite velocities

#vECEFsat :	sat velocity when signal recieved in ECEF frame (v_i)  			--given--
#vECIsat : 	sat velocity when signal recieved in ECI frame (v_i)

	
	###########
	#Array Reference Sheet --------------------------------
	#

#   coords[ith satellite, jth vector, kth coordinate]
#   ranges[ith satellite, jth range]

# Satellite	Location (coords array)			Ranges (ranges array)
#	0 = 25		0 = ECEF epoch position (given)		0 = clock bias (given)
#	1 = 20		1 = ECEF velocity (given)		1 = pseudorange data (given)
#	2 = 11		2 = epoch range vector			2 = epoch range
#	3 = 22		3 = ECEF transmit position		3 = time of flight
#	4 = 1		4 = ECI transmit position		4 = transmit range
#	5 = 32		5 = transmit range vector		5 = computed pseudorange
#	6 = 19		 					6 = observed - computed
#	7 = 14		
#	8 = 31


	##########
	# Import data (needed data and instructor results to compare calcs with)
	#

#imports vectors for each satellite (all vectors for each sat make one row)
coordinates = np.genfromtxt("xyz.csv", delimiter = ',')
#imports all ranges and times for each satellite
givenRanges = np.genfromtxt("ranges.csv", delimiter = ',')
#approximate station parameters
rTONO = np.array([-2296700.0, -4472150.0, 3915300.0, 0])

#Split each sat's row of vectors into array of j vectors (sat# x vector x coordinates)
#	Could also use .reshape??????????????
	
	#empty array for imported vector data
givenCoordinates = np.zeros([9, 6, 3])

	#for each satellite
for i in range(0, 9):
	#and each vector
	for j in range (0, 6):
	#copy each of three coordinates to new dimension
		for k in range (0, 3):
	#2nd dimension of 3D array is now list of 6 coordinates each with values for x, y, z  
			givenCoordinates[ i, j, k] = coordinates[ i, k + j*3]



	##########
	#Start Main Program --------------------------------------------
	#
		

#print header for start of output
header = '###############################START_OUTPUT#######################################'
for i in range(0, 20):
	print(header)
print('\n\n\n\n')


		######################  Problem 1  ###########################

#correct station parameters with least squares method
#	Returns corrected station parameters (x, y, z, bias), covariance matrix, 
#		correlation coefficients, and formal errors
correctedVals = rCorrection(rTONO, givenCoordinates, givenRanges, 9)
#split out corrected parameters
rCorrected = correctedVals[0]

		######################  Problem 2  ###########################

#add random floats between 10 and 20 to station coordinates for unique position 
#	(random.random() gives 0 < n < 1)
#	Can use random.uniform(20,10) if ur lame
MYrTONO = rTONO
for i in range(0,3):
	MYrTONO[i] = rTONO[i] + (random.random()*10 + 10)

#begin printouts to be copied for homework (or start at one ?????????????????????)
print('{} Start Printout Here\n' .format(colored('###################################', 'red')))
#print out new station coordinates
print(' MY unique rTONO coordinates are: \n\n')
print('\t r = {:.3f}, {:.3f}, {:.3f}\n\n' .format(MYrTONO[0], MYrTONO[1], MYrTONO[2]))

#run problem 1 again with new station coordinates
myCorrectedVals = rCorrection(MYrTONO, givenCoordinates, givenRanges, 9)
#split out corrected parameters
MyrCorrected = myCorrectedVals[0]


	
		######################  Problem 3  ###########################

#find differences between previous 2 approximate positions & other values ?????????????

difference = abs(rCorrected - MyrCorrected)
#print(' Parameter difference between corrected given rTONO and corrected MYrTONO: ', difference)

#other differences may be computed if after getting passed out of GPScorrections


		######################  Problem 4  ###########################

noPRN31vals = rCorrection(MYrTONO, givenCoordinates, givenRanges, 8)
rNoPRN31 = noPRN31vals[0]

		######################  Problem 5  ###########################

difference = abs(rNoPRN31 - MyrCorrected)


		######################  Problem 6  ###########################

#transform cartestian coordinates to ellipsoid
#	Returns azmuthal angle (lambda), polar (phi), radius of curvature (N), 
#		and height above ellipsoid (h)
#	Convert tuple to array for nicerness
ellipseVals = np.array(ellipse(rTONO[0:3]))

#convert angle into radians for lat, long (w/ enough decimals for < 1 mm accuracy)

lat = ellipseVals[0] * 180 / np.pi
longi = ellipseVals[1] * 180 / np.pi

print(' Lat, long position of givin station coordinates: \n\n')
print('\t ({:.11f}, {:.1f})\n\n' .format(lat, longi))


		######################  Problem 7  ###########################

	####
	#Find difference from least squares position to original as east, north, up
	#

#create rotation matrix for cartesian -> topocentric using angles from ellipse()
#	Uses lambda and phi from (6) in two rotation matrices (2 & 3)
topoMatrix = np.dot(rot(ellipseVals[0], 2, False), rot(ellipseVals[1], 3, False))

#transform corrected station position to topocentric with orgin at approx station position
rTopo = np.dot(topoMatrix, MyrCorrected[0:3] - rTONO[0:3])

#display difference as east, north, up (index 1, 2, 0)
print(' Corrected position differs from approximate position by:\n\n')
print('\t{} meters East\n\t {} meters North\n\t {} meters up' .format(rTopo[1], rTopo[2], rTopo[0]))
	
		######################  Problem 8  ###########################
	###
	#find satellite 9's (PRN31) elevation angle (theta) and azimuth (alpha) as from station
	#

#transform sat 9 coordinates topocentric with orgin at approx position
satCoords = np.dot(topoMatrix, givenCoordinates[8, 0] - rTONO[0:3])

#need distance from station to satellite (rho)
	#coordinates
rToSat = (givenCoordinates[8, 0] - rTONO[0:3])
	#range
rho = np.sqrt(rToSat[0] ** 2 + rToSat[1] ** 2 + rToSat[2] ** 2)

#compute angles for sat position in the sky
	#arcsin(up/sat-station range)
theta = np.arcsin(satCoords[0] / rho)
	#arctan(east/north)
alpha = np.arctan2(satCoords[1], satCoords[2])


		######################  Problem 9  ###########################
#find cartesian vector from reference point to antenna 1.5 meters up (antenna = corrected position)

#topocentric coordinates of reference point are (east, north, up from antenna):
referenceTopo = np.array([0, 0, -1.5])

#find corrected position elliptical values
correctedEllipse = np.array(ellipse(MyrCorrected[0:3]))

#print difference from approx values
print('\n Difference in approx, corrected ellipse values is: \n\n\t', ellipseVals - correctedEllipse)


#use transpose of topoMatrix with corrected angles to find cartesian coordinates of reference point
#	Gives coordinates in antenna centered frame
correctedTopoMatrix = np.dot(rot(correctedEllipse[0], 2, False), rot(correctedEllipse[1], 3, False))
#transpose
transposedMatrix = np.linalg.inv(correctedTopoMatrix)

#apply tranformation matrix to elliptical coordinates of reference point (0, 0, -1.5)
#	Gives antenna -> reference vector so * (-1)
rReference = np.dot(transposedMatrix, referenceTopo) * -1
print(' Cartesian vector from reference point to antenna: \n\n\t', rReference)


#can also do it:
#reference = antenna (both w/ earth center origin) - third column of transposedMatrix * antenna height
rReference_2 = MyrCorrected[0:3] - (transposedMatrix[ : , 2] * 1.5)

#as gives cartesian coordinates in earth centered frame, must subtract for vector between them
print('or:\t', MyrCorrected[0:3] - rReference_2)


		######################  Problem 10  ###########################

#compute covariance matrix for topocetric coordinates

#make xyz only covariance matrix
covar = myCorrectedVals[1]
xyzCovar = covar[0:3, 0:3]

topoCovar = np.dot(np.dot(correctedTopoMatrix, xyzCovar), transposedMatrix)
print('\n\n Topocentric Covariance Matrix: \n\n\t', topoCovar)

		######################  Problem 11  ###########################
	##---------------
	#Compute formal error and correlation matrix assuming 1 meter data sigmas for all parameters
	#	This is same as cartesian in rCorrection() but uses topocentric coordinates

#create arrays 
topoError = np.zeros(3)
topoCorr  = np.zeros([3, 3])

for i in range(0, 3):
#standard error is sigma and diagonal of covar is sigma^2
	topoError[i] = np.sqrt(topoCovar[i, i])	
	for j in range(0, 3):
#correlation coefficients P_ij = C_ij / root(C_ii * C_jj)
		topoCorr[i, j] = topoCovar[i, j]/np.sqrt(topoCovar[i, i] * topoCovar[j, j])



		######################  Problem 12  ###########################

#cartesian correlation coefficients
cartCorr = myCorrectedVals[2]
#cartesian formal error
cartError = myCorrectedVals[3]

#print comparisons (x, y, z correlations and erros only)
print('\n\n Correlation Coefficients for cartesian : \n\n\t', cartCorr[0:3, 0:3])
print('\n\n and topocentric: \n\n\t', topoCorr)
print('\n\n\n Formal Errors for cartesian: \n\n\t', cartError[0:3])
print('\n\n and topocentric: \n\n\t', topoError)




print('\n\n##############################END of MAIN######################################')

'''
