

import numpy as np

from GPSfns import rot
from termcolor import colored


###
#	This function transforms coordinates from cartesian to ellipsoidal to get lat, long, height.
#		Uses GRS-80 ellipsoid and has precision of > 1 mm
#		Takes in station cartesian coordinates

def ellipse(r):

	print('####################### Start Ellipsoid Transformation ####################\n\n')
#Define ellipse parameters

	#equatorial x-axis which passes through greenwhich meridian (semi-major axis)
	a = 6378137
	#flattening coefficient defined as (a - b)/a
	f = 1 / 298.257222101
	#polar z-axis, derived from f and a
	b =  a * (1 - f)
	#define square of eccentricity (e^2)
	e2 = 1 - b**2/a**2
	#find lambda (lec 7.8)
	lamda = np.arctan2(r[1], r[0])
	#find x-y plane position
	rXY = np.sqrt(r[0]**2 + r[1]**2)



#   
#	ellipsoidal coordinates for station are:
#		longitude angle from equitorial x-axis (lamda) 
#		latitude angle from equatorial plane (phi)
#		length of (N), a line traveling from ellipse surface to polar axis (not ellipse center)
#		height above ellipse surface (h) which continues out from N
#
#	- all angles are to N which is oriented based on being perpendicular to the ellipse surface
# 	- N is also radius of curvature "in prime vertical" ????  and equals: 
#		
#		a^2 / root(a^2*cos^2(phi) + b^2*sin^2(phi)




	###
	#iterate through equations in lec 7.10 to find N, h, phi
	#

#initialize phi for iterative process
#   this is actual formula but with N/(N + h) = 1 (height above ellipsoid = 0)
	phi_0 = np.arctan2(r[2], rXY * (1 - e2**2))
	phi = 0
#iterator
	i = 0
#repeat steps until difference is less than 10E-11 radians as that corresponds to error < .1 mm
	while abs(phi - phi_0) > 10E-10:
		#reset phi for next iteration
		phi = phi_0
		#iterative equations
		N = a**2 / np.sqrt(a**2 * np.cos(phi)**2 + b**2 * np.sin(phi)**2)
		h = rXY / np.cos(phi) - N
		phi_0 = np.arctan2(r[2], rXY * (1 - e2**2) * (N / (N + h)))
		#increase i to count how many times iteration was necessary
		i = i + 1	
	
	print(' {} iterations required for > 1mm accuracy' .format(i))


	###
	#check if angles are correct by transforming back to cartesian and checking vs r
	#

#transform back -> cartesian coordinates (lec 7.8)

	x = (N + h) * np.cos(phi_0) * np.cos(lamda)
	y = (N + h) * np.cos(phi_0) * np.sin(lamda)
	z = ((b**2/a**2) * N + h) * np.sin(phi_0)

	newCoords = np.array([x, y, z])
	

#check all to 2% matching and print ellipsoid values if they match
	if np.allclose(newCoords, r, rtol = .02):
		print(' Coordinate transform sucessfull to ~ 2%\n')
		print(' Ellipsoid values are: \n\n\t phi = {}\n\t lambda = {}' .format(phi_0, lamda))
		print(' \t N = {}\n\t h = {}\n\n\n' .format(N, h))
#if some not matching print % error for each
	else:
		for i in range(0,3):
			error = (abs(newCoords[i] - r[i]) * 100) / r[i]	

			if np.isclose(newCoords[i], r[i], rtol = .02):
				print('\n Coordinate {} matches, error {}'.format(i, error)) 
			else:
				print('\n Coordinate {} {}'.format(i,colored('ERROR','red'))) 
				print(' of {} %' .format(error))

		#return zeros if not matching
		return np.zeros(4)

	print('####################### End of Ellipsoid Transformation ####################\n\n')

	#return ellipsoid values otherwise
	return (phi_0, lamda, N, h)

