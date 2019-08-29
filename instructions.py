For each answer, print out the results and intermediate computations, with annotations to explain the formulas used. Your answers should be clearly labeled (1) through (12).

(1) Reproduce all the computations in the attached spreadsheet. Write down and explain every formula 		that you use. It is critical you get this to work.


(2) Change the approximate coordinates for TONO by any random non-integer amount between 10.000 to	 20.000 meters with some randomly selected digits to three decimal places, so that your 		computations are unique, and different to anybody else’s. Print out the results and all 		intermediate computations and attach them to your answers.


(3) Comment on the differences between (1) and (2), and explain what you see.


(4) Keeping your modified approximate coordinates, remove all data from PRN31 and recompute the 		results. Explain what modifications were necessary to accomplish this.


(5) Comment on the differences between between (3) and (4), and explain what you see.


(6) Using the original approximate Cartesian coordinates of TONO, compute the latitude, longitude, 		and height using the GRS-80 ellipsoid (with parameters given in the lecture on coordinate 		transformations). Be sure to express latitude and longitude in degrees with sufficient 			decimal places to have precision just below 1 mm.


(7) Using the results from (6), compute the rotation matrix that transforms relative Cartesian 		coordinates to topocentric coordinates (east, north, and up) in the neighborhood of TONO. Now 		using this matrix, compute how far in meters the solution from (1) differs from the			 approximate coordinates in the east, north, and up directions.


(8) Compute the elevation angle and azimuth of PRN31 in degrees to one decimal place. Hint: Use the 		rotation matrix from (7).


(9) If TONO has an antenna height of 1.5 meter above a reference mark, compute the relative Cartesian 		coordinates of the vector going from the reference mark up to the antenna. Hence compute		 the Cartesian coordinates of the reference mark using the solution from (1). Hint: Use			 matrix from (7).


(10) Compute the covariance matrix for errors in the topocentric system (east, north, and up). 			Hence compute the formal errors (standard deviations) in east, north and up directions.			Hint: Use matrix from (7).


(11) Compute the correlation coefficients between east, north, and up. Hint:Use matrix from (10).


(12) Comment on how and why the values for formal error and correlation coefficients differ between 		the topocentric and Cartesian systems.





Answers
3)

	final values are within 10^-5
	covariance within 10^-7, 10^-4,-5%
	correlation within 10^-5%
	error within 10^-5%
	partials:
		10^-7 value
		3 and 4 zeros
		no pattern

	Vectors:

		epoch vector:13 - 18 (all identical)
		transmit vector:same as each other and epoch vector to 10^-3,-4
		rest to within 10^-3,-4,-5
		
	differences exactly the same for all sats

	ranges:

		time of flight to 10^-7,-8
		
4)
