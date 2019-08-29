import pandas as pd



#def importClock(file, printIt = False):

#read file into dataframe (can be text file)
data = pd.read_csv('20080101.txt', sep = '\s+', header = None)
	
	
#pull out desired data into new df (all rows where col 4 is 'SAT')
trueFalse = data[4] == 'SAT'
clocks = pd.DataFrame(data[trueFalse])

#run least square regression on each sat's time dataset
for satNum in (23, 24):
	
	#identify rows for sat N with logical vector
	#trueFalse = clocks.iloc[:, 5][-2:] == str(satNum)
	#take last two letters of col 5 and make data frame with similar
	
	
	
	
#perform regression for each satellite
	
		
#pick most stable clocks


#look at periodicities in time


#redo process with frequencies


#look 





#x = importClock('20080101.txt')