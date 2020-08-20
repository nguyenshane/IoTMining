#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 16:09:31 2020

@author: qb
"""
import os
import numpy as np
import utils
from datetime import datetime, timedelta

def updateDates(_startDate, _endDate):
    """ Return new pair of start and end dates with +7 each """
    newStartDate = (datetime.strptime(_startDate, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')
    newEndDate = (datetime.strptime(_endDate, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')
    return str(newStartDate), str(newEndDate) 


def getEndDate(_startDate):
    """Return the end date, which is +7 from the start date"""
    res = (datetime.strptime(_startDate, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')
    
    return str(res)

def dataPartition(filename):
    dataTable = np.load(filename, allow_pickle = True)
    startDate = utils.startDate
    endCondition = datetime.strptime(utils.endDate, '%Y-%m-%d')
    endDate = getEndDate(startDate)
    weekIndex = 1
    while (datetime.strptime(startDate, '%Y-%m-%d') < endCondition):
        exportTable = []
        for row in range(0,dataTable.shape[0]):
            dateStr = str(dataTable[row][0]).split()[0]
            currentDate = datetime.strptime(dateStr, '%Y-%m-%d')
            if currentDate >= datetime.strptime(startDate, '%Y-%m-%d') and currentDate < datetime.strptime(endDate, '%Y-%m-%d'):
                exportTable.append(dataTable[row])
        
        exportTable = np.array(exportTable, dtype=object)
        np.save('./npy/dataByWeek/week' + str(weekIndex), exportTable)
        print('Saved week ' + str(weekIndex))
        dateTup = updateDates(startDate, endDate)
        startDate = dateTup[0]
        endDate = dateTup[1]
        weekIndex += 1
        
        
        
        
    
    

if __name__ == '__main__':
       
    filename = "./npy/datanpy.npy"
    dataName = filename.split("/")[-1]
    if not os.path.exists('./npy/dataByWeek/'):
            os.makedirs('./npy/dataByWeek')
    print("Partitioning " + dataName + "...")
    dataPartition(filename)
    print("Done")
 



#quick test here 
#print("Start date: " + utils.startDate)
#print("End date: " + getEndDate(utils.startDate))
#print("next week: " + str(updateDates(utils.startDate,getEndDate(utils.startDate))))
