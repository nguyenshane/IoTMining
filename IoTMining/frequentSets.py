#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils
import os
from datetime import datetime, time, timedelta
import numpy as np
from numpy.core.defchararray import find
from efficient_apriori import apriori


def findFrequentSets(weeks):
    dataTable = None
    baskets = {} # dictionary
    for week in weeks:
        filename = "./npy/prunedDataByWeek/week" + str(week) + ".npy"
        try:
            weekDataTable = np.load(filename, allow_pickle = True)
        except:
            print(filename, "doesn't exist.")
            
            
        if (len(weekDataTable) > 0):
            for dayInWeek in range(0,6):
                for partitionTimeIndex in utils.timePartitionMap:
                    idx = (weekDataTable[:, 1] == dayInWeek) & (weekDataTable[:, 2] == int(partitionTimeIndex))
                    
                    currentDataTable = weekDataTable[idx]
                    id = str(dayInWeek) + partitionTimeIndex
                    # print('currentDataTable', tuple(set(currentDataTable[:, 3])))
                    
                    if (len(currentDataTable) == 0):
                        continue
                    
                    uniqueSegments = np.unique(currentDataTable[:,3])
                    
                    for uniqueSegment in uniqueSegments:
                        if (not id in baskets):
                            baskets[id] = [tuple(set(currentDataTable[:, 4]))]
                        else:
                            baskets[id].extend([tuple(set(currentDataTable[:, 4]))])
            
        # if ((dataTable is None) & (len(weekDataTable) > 0)):
        #     dataTable = weekDataTable
        # elif (len(weekDataTable) > 0):
        #     dataTable = np.concatenate([dataTable, weekDataTable])
        
    
    
                    
                
    for id in baskets:
        #print("Basket", baskets[id])
        
        itemsets, rules = apriori(baskets[id], min_support=0.8, min_confidence=1, max_length=2)
        print(rules)
                    
            
    # print("Baskets", baskets)
    return

        
    
findFrequentSets(tuple(range(11,15)))