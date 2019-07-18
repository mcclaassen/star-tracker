# This program computes GPS coordinates using functions in:
#	GPScalcs.py
#	GPSfns.py
# All calculations are in relation to TONO station near Tonopah, NV 


import numpy as np

from GPScalcs import calcs



#takes: approximate station parameters, two givin arrays, and number of satellite observations
def rCorrection(approxPars, vectors, ranges, n):

#precise TONO station coordinates and clock bias given by JPL
	JPLrTONO = np.array([-2296771.3941, -4472097.1915, 3915214.3049, 15.4670])

#arrays for computed values
	cVectors = np.zeros([n, 4, 3])
	cRanges = np.zeros([n, 5])
	cPartials = np.zeros([n, 4])


	###---------------
	# Calculate spreadsheet values, loop for all satellites
	#

	for i in range (0, n):

	#store vector, range, and partial arrays returned from calcs() as tuple of arrays
		arrays = calcs(i, vectors[0:n], ranges[0:n], approxPars[0:3])
	#split into individual arrays
		cVectors[i] = arrays[0]
		cRanges[i] = arrays[1]
		cPartials[i] = arrays[2]

#needed for symbolic partials script
#	for j in range(0,4):
#		cPartials[i, j] = pars[j]

#transpose partials array
	partialsT = np.transpose(cPartials)

#print computed values

	print('\n\n Initial epoch range vectors (meters): \n')
	for i in range(0, n):
		print('\tSatellite {}:\t{}' .format(i + 1, np.round(cVectors[i, 0], 3)))

	print('\n\n Initial epoch ranges (meters): \n')
	for i in range(0, n):
		print('\tSatellite {}:\t{}' .format(i + 1, np.round(cRanges[i, 0], 3)))

	print('\n\n Initial times of flight (seconds): \n')
	for i in range(0, n):
		print('\tSatellite {}:\t{}' .format(i + 1, np.round(cRanges[i, 1], 3)))

	print('\n\n ECEF transmit positions (meters): \n')
	for i in range(0, n):
		print('\tSatellite {}:\t{}' .format(i + 1, np.round(cVectors[i, 1], 3)))

	print('\n\n ECI transmit positions (meters): \n')
	for i in range(0, n):
		print('\tSatellite {}:\t{}' .format(i + 1, np.round(cVectors[i, 2], 3)))

	print('\n\n Revised (transmit) range vectors (meters): \n')
	for i in range(0, n):
		print('\tSatellite {}:\t{}' .format(i + 1, np.round(cVectors[i, 3], 3)))

	print('\n\n Revised (transmit) ranges (meters): \n')
	for i in range(0, n):
		print('\tSatellite {}:\t{}' .format(i + 1, np.round(cRanges[i, 2], 3)))

	print('\n\n Computed pseudoranges (meters): \n')
	for i in range(0, n):
		print('\tSatellite {}:\t{}' .format(i + 1, np.round(cRanges[i, 3], 3)))

	print('\n\n Observed - computed values (meters): \n')
	for i in range(0, n):
		print('\tSatellite {}:\t{}' .format(i + 1, np.round(cRanges[i, 4], 3)))

	print('\n\n Partials matrix: \n')
	for i in range(0, n):
		print('\tSatellite {}:\t{}' .format(i + 1, np.round(cPartials[i], 3)))
	
	print('\n\n Transposed partials matrix: \n\n')
	print('\t x \t', np.round(partialsT[0], 3))
	print('\t y \t', np.round(partialsT[1], 3))
	print('\t z \t', np.round(partialsT[2], 3))
	print('\t tau \t', np.round(partialsT[3], 3))
	
	
	##------------------
	#Improve station position estimate and generate covariance matrix
	#

#compute each side of normal equations seperately
#  Normal equation is:
#  partialsT*cPartials*delta = partialsT*(oc) or (AT*A)*xHat = AT(o - c)

	#left side
	ATA = np.dot(partialsT, cPartials) 
	print('\n\n Left side of Normal equation:\n\n')
	print('\t x \t', np.round(ATA[0], 3))
	print('\t y \t', np.round(ATA[1], 3))
	print('\t z \t', np.round(ATA[2], 3))
	print('\t tau \t', np.round(ATA[3], 3))


#construct covariance matrix assuming 1 meter data sigma for all parameters
	covar = np.linalg.inv(ATA)
	print('\n\n Covariance Matrix: \n\n')
	print('\t x \t', np.round(covar[0], 3))
	print('\t y \t', np.round(covar[1], 3))
	print('\t z \t', np.round(covar[2], 3))
	print('\t tau \t', np.round(covar[3], 3))

	#right side
	Aoc = np.dot(partialsT, cRanges[ : , 4])
	print('\n\n Right side of Normal equation: \n')
	print('\t x \t', np.round(Aoc[0], 3))
	print('\t y \t', np.round(Aoc[1], 3))
	print('\t z \t', np.round(Aoc[2], 3))
	print('\t tau \t', np.round(Aoc[3], 3))
	

#solve normal eq. for delta (xHat) and add to initial parameters for final parameters
	delta = np.dot(np.linalg.inv(ATA),Aoc)
	print('\n\n Parameter adjustments (delta estimate): \n')
	print('\t x \t', np.round(delta[0], 3))
	print('\t y \t', np.round(delta[1], 3))
	print('\t z \t', np.round(delta[2], 3))
	print('\t tau \t', np.round(delta[3], 3))

	final = approxPars + delta
	print('\n\n Final estimated parameters: \n\n\t', final)

	##---------------
	#Compute formal error and correlation matrix assuming 1 meter data sigmas per parameter
	#

#create arrays
	error = np.zeros(4)
	corr  = np.zeros([4,4])

	for i in range(0,4):
#standard error is sigma and diagonal of covar is sigma^2
		error[i] = np.sqrt(covar[i, i])	
		for j in range(0,4):
#correlation coefficients P_ij = C_ij / root(C_ii * C_jj)
			corr[i, j] = covar[i, j]/(np.sqrt(covar[i, i] * covar[j, j]))

	print('\n\n Formal Error in parameters (sigma): \n\n\t', error)

#find difference from JPL computed position
	errorJPL = final - JPLrTONO
	print('\n\n JPL estimated parameters: \n\n\t', JPLrTONO)
	print('\n\n Difference between my parameters and JPL\'s: \n\n\t', errorJPL)

	print('\n\n Correlation Coefficients are: \n')
	print('\t x \t', np.round(corr[0], 3))
	print('\t y \t', np.round(corr[1], 3))
	print('\t z \t', np.round(corr[2], 3))
	print('\t tau \t', np.round(corr[3], 3))

	print('\n\t\t    ***** End of Position Correction ***** \n\n\n\n\n')

	return (final, covar, corr, error)
