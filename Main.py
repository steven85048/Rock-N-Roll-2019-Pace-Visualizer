import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from DataRetrieval import DataRetrieval

Retrieval = DataRetrieval( )
Retrieval.retrieveData()
runners = Retrieval.getPoints()

timePoints = []
for runner in runners:
    finishTime = runner['finishTime']
    timeParts = finishTime.split(":")

    hours = int( timeParts[0].lstrip("0") )
    minutes = int( timeParts[1].lstrip("0") )
    seconds = int( timeParts[2].lstrip("0") )

    thePoint = 60 * hours + minutes + ( seconds / 60 )
    timePoints.append( thePoint )

numBins = 50
n, bins, patches = plt.hist( timePoints, numBins, faceColor = 'blue', alpha = 0.5 )
plt.show()