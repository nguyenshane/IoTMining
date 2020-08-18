from utils import labelSet
from utils import timeStampDiff
from utils import timePruningThreshold
import numpy as np


def timePruning():
    """Return a list of routine items i.e. a basket for A-priori """
    # an item is routine if its duration is longer then the time pruning threshold
    # a routine item can be occupancy: motion sensors ;and usage: lightning sensor
    routineItems = []
    dataTable = np.load("./npy/datatimeprunetestnpy.npy", allow_pickle = True)
    
    for elem in labelSet:
        totalDuration = 0
        timeStampList = []
        endPoint = dataTable.shape
        
        for row in range(0,endPoint[0]):
            if elem == dataTable[row][3]:
                timeStamp = str(dataTable[row][0]).split()
                timeStampList.append(timeStamp[1])
                
        #compute the duration of the intervals between triggered for a sensorID
        for i in range(0,len(timeStampList) - 1):
            totalDuration += timeStampDiff(timeStampList[i],timeStampList[i+1])
            
        if totalDuration > timePruningThreshold :
            routineItems.append(elem)
            
    return routineItems
