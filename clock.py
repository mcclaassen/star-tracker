import pandas as pd
import numpy as np



#def importClock(file, printIt = False):


dataSets = []

#read file into dataframe (can be text file)
data = pd.read_csv('20080101.txt', sep = '\s+', header = None)
	
	
#pull out desired data into new df (all rows where col 4 is 'SAT')
#unnecessary ??????
	#####trueFalse = data[4] == 'SAT'
	#####clocks = pd.DataFrame(data[trueFalse])

#run least square regression on each sat's time dataset
for satNum in range(23, 25):
	
	#identify rows for sat N with logical vector
	trueFalse = data.iloc[:, 5] == 'BIASGPS' + str(satNum)
	#take last two letters of col 5 and make data frame with similar
	
	#make list of arrays of sat datasets
	dataSets.append(np.array(data[trueFalse]))
	
	
#perform regression for each satellite
	
		
#pick most stable clocks


#look at periodicities in time


#redo process with frequencies


#look 





#x = importClock('20080101.txt')