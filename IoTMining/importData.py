#!/usr/bin/env python3

import os
import utils
from datetime import datetime, time, timedelta
from utils import sensorFilter
import numpy as np

datasets = ["./dataset/data"]
datasetsNames = [i.split('/')[-1] for i in datasets]

def loadDataset(filename):
    dataTable = []
    with open(filename, 'rb') as features:
        database = features.readlines()
        for i, line in enumerate(database):  # each line
            lineList = line.decode().split()  # split a line into a list separated by spaces.
            # A line looks like this 
            # 2009-08-24 00:00:19.034964	M050	ON	R1_Wandering_in_room begin
            # Turn them into the following fields
            timestamp = None
            originalSensor = None
            sensor = None
            value = None
            activity = None
            dayOfWeek = None
            partitionTimeOfDay = None
            try:
                if 'M' == lineList[2][0] or 'L' == lineList[2][0]:
                    # choose only M, L sensors
                    
                    originalSensor = str(np.array(lineList[2]))
                    sensor = sensorFilter(originalSensor)
                    
                    if (sensor is None):
                        continue
                    
                    if not ('.' in str(np.array(lineList[0])) + str(np.array(lineList[1]))):
                        lineList[1] = lineList[1] + '.000000'
                    timestamp = (datetime.strptime(str(np.array(lineList[0])) + str(np.array(lineList[1])),
                                                        "%Y-%m-%d%H:%M:%S.%f"))
                    dayOfWeek = timestamp.weekday()
                    partitionTimeOfDay = utils.timeInPartition(timestamp.hour)
                    
                    value = (str(np.array(lineList[3])))

                    if len(lineList) == 4:  # if activity does not exist
                        activity = ''
                    else:  # if activity exists
                        activity = str(' '.join(np.array(lineList[4:])))
                        if 'begin' in activity:
                            #activity = re.sub('begin', '', des)
                            if activity[-1] == ' ':  # if white space at the end
                                activity = activity[:-1]  # delete white space
                        if 'end' in activity:
                            if activity[-1] == ' ':  # if white space at the end
                                activity = activity[:-1]  # delete white space
                    dataTable.append([timestamp,
                                      dayOfWeek, 
                                      partitionTimeOfDay,
                                      originalSensor,
                                      sensor,
                                      value,
                                      activity])
            except IndexError:
                print(i, line)

            
    features.close()
   
    return dataTable
    
def partitionDataByWeek(path):
    dataTable = np.load(path, allow_pickle=True)
    startDate = datetime.combine(dataTable[0][:1][0].date(), time(0))
    finalDate = datetime.combine(dataTable[dataTable.shape[0]-1][:1][0].date() 
                                 + timedelta(days=1), time(0))
    
    currentWeek = 0
    
    while True:
        nextEndDate = startDate + timedelta(days=7)
        idx = ((dataTable[:, 0] >= startDate)
            & (dataTable[:, 0] < nextEndDate)
            & (dataTable[:, 0] < finalDate))
        
        if not os.path.exists('./npy/dataByWeek/'):
            os.makedirs('./npy/dataByWeek/')
        
        np.save('./npy/dataByWeek/week' + str(currentWeek), dataTable[idx])
        print('Saved ./npy/dataByWeek/week' + str(currentWeek))

        if (nextEndDate >= finalDate):
            break
        else:
            startDate = nextEndDate
            currentWeek += 1

if __name__ == '__main__':

    if not os.path.exists('npy/datanpy.npy'):
        # Generate the full dataset
        for filename in datasets:
            datasetName = filename.split("/")[-1]
            print('Loading ' + datasetName + ' dataset ...')
            dataTable = loadDataset(filename)

            dataTable = np.array(dataTable, dtype=object)
            if not os.path.exists('npy'):
                os.makedirs('npy')

            np.save('./npy/' + datasetName + 'npy', dataTable)
            print('Saved ' + datasetName)
    # Partition full dataset to week
    partitionDataByWeek('npy/datanpy.npy')
