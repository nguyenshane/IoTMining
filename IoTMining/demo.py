#!/usr/bin/env python3

# Research: Incremental Learning from IoT for Smart Home Automation
# Authors: Nguyen Do, Quan Bach
# Usage:
# Demo


import numpy as np
import utils
import calendar
from datetime import date, datetime



def demo(inputKey):
    dataTable = np.load('./npy/demoData/set31.npy', allow_pickle=True)

    
    if inputKey == '1':
        today =  date.today()
        now = datetime.now()
        dayOfWeek = now.weekday()
        partitionTimeOfDay = utils.timeInPartition(now.hour)
        #key to the association rule map
        #key: 00 01 02 10 11 12 20 21 22 30 31 32 40 41 42 50 51 52 60 61 62
        key  = str(dayOfWeek) + str(partitionTimeOfDay)
        returnTable = dataTable[(dataTable[:,0] == key)]
        print('Current time  is: '+ str(calendar.day_name[dayOfWeek]) + ' ' +str(now))
    else:
        key = inputKey
        returnTable = dataTable[(dataTable[:,0] == key)]

   
        
    assoArr = returnTable[0][1].replace('[','')
    assoArr = assoArr.replace(']','')
    assoArr = assoArr.strip()
    assoArr = assoArr.split(',')
         
    print('System rules: ')
    for i in range(1,len(assoArr)):
        print(assoArr[i])

if __name__ == '__main__':
    while (1):
        print('\n'*6)
        print("----- WELCOME TO YOUR SMART HOME CENTRAL CONTROL SYSTEM ------")
        print('\t' + " 1. Automated rules at current time")
        print('\t' + " 2. Automated rules by key")
        print('\t' + " 3. Exit")
        num = input ("Enter your option : ") 
        if num == '3':
            print('\n'*4)
            print('\t' + "Have a nice day Mr.Hwang ")
            print('\n'*4)
            break
        elif num == '1':
            demo(num)
        elif num == '2':
            #key: 00 01 02 10 11 12 20 21 22 30 31 32 40 41 42 50 51 52 60 61 62
            key = input("Please enter the key: ")
            demo(key)
            

    