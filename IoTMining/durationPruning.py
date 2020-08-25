#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 13:35:15 2020

@author: QB
"""

from utils import labelSet, timeStampDiff, durationThreshold, basketsKeySet
from collections import defaultdict
import numpy as np

filename = "./npy/datatestnpy.npy"

def durationPruning(filename):
    """Return a map of routine items i.e. a baskets for A-priori"""
    """keys of the map are the combinations of dayOfWeek + partitionTimeOfDay i.e. 00, 01, 02...62 """
    # an item is routine if its duration is longer then the time pruning threshold
    # a routine item can be occupancy: motion sensors ;and usage: lightning sensor

    routineItemsMap = defaultdict(list)
    dataTable = np.load(filename, allow_pickle = True)

    for key in basketsKeySet:
        timeStampList = []
        routineItems = []
        for elem in labelSet: # scan the data for each sensor ID
            totalDuration = 0
            endPoint = dataTable.shape
            lookingForOn = True # flag to alternate looking for ON and not ON (i.e. OFF)
            for row in range(0,endPoint[0]):
                keyInTable = str(dataTable[row][1])+str(dataTable[row][2])
                if key == keyInTable:
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
        
            if totalDuration > durationThreshold : #time pruning
                routineItems.append(elem)
                
        routineItemsMap[key].append(routineItems)
    return routineItemsMap

# un-comment the line below to test output
#filename = "./npy/datatestnpy.npy"
#print(durationPruning(filename))
