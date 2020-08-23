#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils
import os
from datetime import datetime, time, timedelta
import numpy as np
from numpy.core.defchararray import find


def preProcessing(week, dataTable):
    if (dataTable is None):
        filename = "./npy/dataByWeek/week" + str(week) + ".npy"
        dataTable = np.load(filename, allow_pickle = True)
    
    prunedDataTable = []
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
            break;
            
    prunedDataTable = np.array(prunedDataTable, dtype=object)
    if not os.path.exists('npy/prunedDataByWeek'):
        os.makedirs('npy/prunedDataByWeek')
    np.save('./npy/prunedDataByWeek/week' + str(week), prunedDataTable)
    print('prunedDataTable', prunedDataTable)
            
    return

def pruneByDevice(segment, segmentCount):    
    deviceList = segment[:, 3]
    for index, device in enumerate(deviceList):
        if (device != None):
            if ('Light' in device) or ('fan' in device):
                segment = pruneDuplication(segment)
                newCol = np.full((1, len(segment)), segmentCount)
                segment = np.insert(segment, 3, newCol,  axis=1)
                return segment.tolist()
    
    return []

def pruneDuplication(segment):
    onIdx = (segment[:, 4] == "ON")
    onSegment = segment[onIdx]
    uniqueKeys, indices = np.unique(onSegment[:, 3], return_index=True)
    
    newSegment = onSegment[indices]
    return newSegment
        
    
# preProcessing(11, None)