#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 16:19:19 2020

@author: QB
"""

from durationPruning import upgradedDurationPruning
from efficient_apriori import apriori
from utils import basketsKeySet, sizeOfSlidingWindow, basketsKeySet
from collections import defaultdict
import os

def assoRulesGenerator():
    path = './npy/dataByWeek/'
    weekCount = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    
    #compute the total number of sliding window
    windowCount = weekCount - sizeOfSlidingWindow + 1  #algor:(n-k+1) with k is the size of sliding window
    
    if not os.path.exists('./dpRules/'):
            os.makedirs('./dpRules/')
    
    
    for i in range(0,windowCount):
        freqSetMap = defaultdict(list)
        assoMap = {}
        for j in range(i, i+4):
            filename = path + 'week' + str(j) + '.npy'
            table1, table2 = upgradedDurationPruning(filename)
            #currentWeek = '===== Week ' + str(j) + ' ====='
            #print(currentWeek)
            #for key in basketsKeySet:
                    #print("{} : {}".format(key,table2[key]))
            for key in basketsKeySet: 
                freqSetMap[key].append(table2[key])
            
        for key in freqSetMap:
            freqList = []
            for elem in freqSetMap[key]:
                if elem is not []:
                    freqList.append(tuple(elem))
                    
            items, rules = apriori(freqList, min_support=0.5, min_confidence=1)
            assoMap[key] = rules
            
        currentWindow = '===== Window ' + str(i+1) + ' ====='
        print(currentWindow)
        for key in assoMap:
            print("{} : {}".format(key,assoMap[key]))
        
        outFile = open('./dpRules/assoRules.txt','a+')
        outFile.write(currentWindow)
        outFile.write('\n')
        for key in assoMap:
            outFile.writelines("{} : {}".format(key,assoMap[key]))
            outFile.write('\n')
        outFile.write('\n')
        outFile.close()

assoRulesGenerator()