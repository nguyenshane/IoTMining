#!/usr/bin/env python3

# Research: Incremental Learning from IoT for Smart Home Automation
# Authors: Nguyen Do, Quan Bach
# Usage:
# Time Threshold Pruning
# By running this file, it will pick up datasets in npy/prunedDataByWeek,
# prune the data based on minute time threshold, combine with deduplication
# and filter segments that doesn't have interesting device type to learn

import utils
import os
from datetime import timedelta
import numpy as np
import time

def timeThresholdPruning(week, dataTable):
    startProcessTime = time.process_time()
    if (dataTable is None):
        filename = "./npy/dataByWeek/week" + str(week) + ".npy"
        try:
            dataTable = np.load(filename, allow_pickle = True)
        except:
            prunedDataTable = np.array([], dtype=object)
            if not os.path.exists('npy/prunedDataByWeek'):
                os.makedirs('npy/prunedDataByWeek')
            np.save('./npy/prunedDataByWeek/week' + str(week), prunedDataTable)
            return
        
    dataSize = len(dataTable)
    
    prunedDataTable = []
    if (len(dataTable) == 0):
        return
    startTime = dataTable[0][:1][0]

    dataTableIndex = 0
    segmentCount = 0
    
    while True:

        nextTimeSegment = startTime + timedelta(minutes= utils.timePruningThreshold)
        #print('next time', nextTimeSegment)
        idx = (dataTable[:, 0] >= startTime) & (dataTable[:, 0] < nextTimeSegment)
        
        currentSegment = dataTable[idx]
        
        dataTableIndex += len(currentSegment) - 1
        #print('segment', currentSegment, segmentCount)
        
        prunedSegment = pruneByDevice(currentSegment, segmentCount)
        
        if (len(prunedSegment) > 0):
            prunedDataTable.extend(prunedSegment)

        if (len(dataTable) > 1):
            segmentCount += 1
        
            # trim off dataTable as we go
            dataTable = dataTable[len(currentSegment): len(dataTable), :]
            
            if (len(dataTable) == 0):
                break
            startTime = dataTable[0][:1][0]
        else:
            break
            
    prunedDataTable = np.array(prunedDataTable, dtype=object)
    if not os.path.exists('npy/prunedDataByWeek'):
        os.makedirs('npy/prunedDataByWeek')
    np.save('./npy/prunedDataByWeek/week' + str(week), prunedDataTable)
    
    endProcessTime = time.process_time() - startProcessTime
    print('week:', week, 'excecution time:', endProcessTime)
    if not os.path.exists('./ProgOutput/'):
        os.makedirs('./ProgOutput/')    
    outFile = open('./ProgOutput/pruneTimeThreshold-Measure.txt','a+')
    outFile.writelines("{}, {}, {}\n".format(week, dataSize, endProcessTime))
    outFile.close()
    print('prunedDataTable', prunedDataTable)

    return

def pruneByDevice(segment, segmentCount):    
    deviceList = segment[:, 4]
    for index, device in enumerate(deviceList):
        if (device != None):
            if ('Light' in device) or ('fan' in device):
                segment = pruneDuplication(segment)
                newCol = np.full((1, len(segment)), segmentCount)
                segment = np.insert(segment, 3, newCol,  axis=1)
                return segment.tolist()
    
    return []

def pruneDuplication(segment):
    onIdx = (segment[:, 5] == "ON")
    onSegment = segment[onIdx]
    uniqueKeys, indices = np.unique(onSegment[:, 4], return_index=True)
    
    newSegment = onSegment[indices]
    return newSegment

if __name__ == '__main__':
    path = './npy/dataByWeek/'
    weekCount = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    for i in range (0, weekCount):
        filename = "./npy/dataByWeek/week" + str(i) + '.npy'

        timeThresholdPruning(i, None)
        
    
#timeThresholdPruning(9, None)