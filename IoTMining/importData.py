#!/usr/bin/env python3

import datetime
import os
import re
from collections import Counter
from datetime import datetime

import numpy as np
from keras.preprocessing import sequence

offset = 20
max_lenght = 2000

datasets = ["./dataset/datatest"]
datasetsNames = [i.split('/')[-1] for i in datasets]


def load_dataset(filename):
    dataTable = []
    with open(filename, 'rb') as features:
        database = features.readlines()
        for i, line in enumerate(database):  # each line
            lineList = line.decode().split()  # split a line into a list separated by spaces.
            # A line looks like this 
            # 2009-08-24 00:00:19.034964	M050	ON	R1_Wandering_in_room begin
            # Turn them into the following fields
            timestamp = None
            sensor = None
            value = None
            activity = None
            try:
                if 'M' == lineList[2][0] or 'L' == lineList[2][0]:
                    # choose only M, L sensors
                    if not ('.' in str(np.array(lineList[0])) + str(np.array(lineList[1]))):
                        lineList[1] = lineList[1] + '.000000'
                    timestamp = (datetime.strptime(str(np.array(lineList[0])) + str(np.array(lineList[1])),
                                                        "%Y-%m-%d%H:%M:%S.%f"))
                    sensor = (str(np.array(lineList[2])))
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
                    dataTable.append([timestamp, sensor, value, activity])
            except IndexError:
                print(i, line)

            
    features.close()
   
    return dataTable


if __name__ == '__main__':
    for filename in datasets:
        datasetName = filename.split("/")[-1]
        print('Loading ' + datasetName + ' dataset ...')
        dataTable = load_dataset(filename)

        # X, Y, dictActivities = convertActivities(X, Y,
        #                                          dictActivities,
        #                                          mappingActivities[datasetName],
        #                                          cookActivities[datasetName])

        # print(sorted(dictActivities, key=dictActivities.get))
        # print("n° instances post-filtering:\t" + str(len(X)))

        # print(Counter(Y))

        # X = np.array(X, dtype=object)
        # Y = np.array(Y, dtype=object)

        # X = sequence.pad_sequences(X, maxlen=max_lenght, dtype='int32')

        dataTable = np.array(dataTable, dtype=object)
        if not os.path.exists('npy'):
            os.makedirs('npy')

        np.save('./npy/' + datasetName + 'npy', dataTable)
        # np.save('./npy/' + datasetName + '-y.npy', Y)
        # np.save('./npy/' + datasetName + '-labels.npy', dictActivities)


def getData(datasetName):
    X = np.load('./npy/' + datasetName + '-x.npy')
    Y = np.load('./npy/' + datasetName + '-y.npy')
    dictActivities = np.load('./npy/' + datasetName + '-labels.npy').item()
    return X, Y, dictActivities
