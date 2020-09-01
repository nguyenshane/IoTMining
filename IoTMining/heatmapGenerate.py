#!/usr/bin/env python3

# Research: Incremental Learning from IoT for Smart Home Automation
# Authors: Nguyen Do, Quan Bach
# Usage:
# Heatmap Generator
# By running this file, it will pick up datasets in npy/prunedDataByWeek,
# and generate heat maps for analysis purpose

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image

#2D Gaussian function
def twoD_Gaussian(x, y, xo, yo, sigma_x, sigma_y):
    a = 1./(2*sigma_x**2) + 1./(2*sigma_y**2)
    c = 1./(2*sigma_x**2) + 1./(2*sigma_y**2)
    g = np.exp( - (a*((x-xo)**2) + c*((y-yo)**2)))
    return g.ravel()


def transparent_cmap(cmap, N=255):
    "Copy colormap and set alpha values"

    mycmap = cmap
    mycmap._init()
    mycmap._lut[:,-1] = np.linspace(0, 0.6, N+4)
    return mycmap


if __name__ == "__main__":
    
    dataTable = np.load('./npy/dataByWeekNoFilter/week0.npy', allow_pickle=True)
    sensorArr = dataTable[:,3]
    unique, counts = np.unique(sensorArr, return_counts=True)
    countDict = dict(zip(unique, counts))
    
    if bool(countDict):
        maxCount = max(countDict.values())
    
    locationDict = {}
    filename = "./sensorLocation.txt"
    with open(filename, 'rb') as locations:
        lines = locations.readlines()
        for line in lines:
            lineList = line.decode().split()
            locationDict.update({str(lineList[0]): (float(lineList[1]),float(lineList[2]))})
    
        
    #Use base cmap to create transparent
    redcmap = transparent_cmap(plt.cm.Oranges)
    bluecmap = transparent_cmap(plt.cm.Blues)


    # Import image and get x and y extents
    I = Image.open('./heatmap.png')
    p = np.asarray(I).astype('float')
    w, h = I.size
    y, x = np.mgrid[0:h, 0:w]

    #Plot image and overlay colormap
    fig, ax = plt.subplots(1, 1)

    for key in locationDict:
        if key in countDict.keys(): 
            Gauss = twoD_Gaussian(x, y, locationDict[key][0] *x.max(), locationDict[key][1] *y.max(), .08*x.max(), .08*y.max())
            if str(key)[0] == "M":
                value = int(((countDict[key])/maxCount)*200)
                cb = ax.contourf(x, y, Gauss.reshape(x.shape[0], y.shape[1]), value , cmap=redcmap)
            else:
                value = int(((countDict[key]*101)/maxCount)*100)
                cb = ax.contourf(x, y, Gauss.reshape(x.shape[0], y.shape[1]),  value , cmap=bluecmap)


    plt.axis('off')
    ax.imshow(I)
    plt.show()

