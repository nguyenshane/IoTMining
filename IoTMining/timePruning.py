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
        lookingForOn = True # flag to alternate looking for ON and not ON (i.e. OFF)
        #firstOFFMark = None #for later usage
        for row in range(0,endPoint[0]):
           
            #in case reach the end but OFF not found (i.e. device has only ON)
            if row == (endPoint[0]-1) and not lookingForOn:
                timeStamp = str(dataTable[row][0]).split()
                timeStampList.append(timeStamp[1])
                
                
            #looking for ON
            if elem == dataTable[row][3] and lookingForOn and "ON" == str(dataTable[row][4]):
                timeStamp = str(dataTable[row][0]).split()
                timeStampList.append(timeStamp[1])
                lookingForOn = False
                
            #looking for OFF
            if elem == dataTable[row][3] and not lookingForOn and "OFF" == str(dataTable[row][4]):
                timeStamp = str(dataTable[row][0]).split()
                timeStampList.append(timeStamp[1])
                lookingForOn = True
                
            #compute the duration of the intervals between ON and OFF
            if len(timeStampList) == 2:
                totalDuration += timeStampDiff(timeStampList[0],timeStampList[1])
                timeStampList.clear()
            
        if totalDuration > timePruningThreshold : #time pruning
            routineItems.append(elem)
