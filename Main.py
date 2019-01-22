import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from DataRetrieval import DataRetrieval, FilterType, Gender, Division

Retrieval = DataRetrieval( )
Retrieval.retrieveData()

# set filters
Retrieval.addDivisionFilter(Division.SC18_24)
Retrieval.addGenderFilter(Gender.MALE)

runners = Retrieval.getPoints()

timePoints = []
for runner in runners:
    finishTime = runner['results']['finishTime']
    timeParts = finishTime.split(":")

    if( len(timeParts) != 3 or timeParts[0] == '' or timeParts[1] == '' or timeParts[2] == '' ):
        continue

    hours = int(  timeParts[0].lstrip("0") if timeParts[0] != '00' else '0' )
    minutes = int( timeParts[1].lstrip("0") if timeParts[1] != '00' else '0' )
    seconds = int( timeParts[2].lstrip("0") if timeParts[2] != '00' else '0' )

    thePoint = 60 * hours + minutes + ( seconds / 60 )
    timePoints.append( thePoint )

numBins = 50
n, bins, patches = plt.hist( timePoints, numBins, faceColor = 'blue', alpha = 0.5 )
plt.show()