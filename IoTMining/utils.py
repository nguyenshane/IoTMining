# -*- coding: utf-8 -*-

sizeOfSlidingWindow = 4 #the number of weeks in the sliding window for apriori
timePruningThreshold = 1 # time threshold in minute
durationThreshold = 15 # duration threshold in minute

startDate = "2009-08-24" # start and end date got from the study 
endDate = "2010-05-01"

timePartitionMap = {"0": {"start": 6, "end": 11}, # Morning
                    "1": {"start": 12, "end": 19}, # Afternoon
                    "2": {"start": 20, "end": 5}} # Everning

lightningMap = {"L001" : "R1room_Light",
                "L002" : "R3room_Light",
                "L003" : "uHall_Light",
                "L004" : "R2room_Light",
                "L005" : "BA_sink_Light",
                "L006" : "BA_tub_Light",
                "L007" : "BA_fan",
                "L008" : "Liv_Light",
                "L009" : "dHall_Light",
                "L010" : "Kitchen_Light"}

"""
Organizing sensors IDs into sets.

"""

LivingRoomSensorSet =    ( "M001",
                           "M002",
                           "M003",
                           "M004",
                           "M005",
                           "M006",
                           "M007",
                           "M008",
                           "M009",
                           "M010",
                           "M011",
                           "M012",
                           "M013",
                           "M014",
                           "M015")
R1roomSensorSet =     ("M044",
                       "M045",
                       "M046",
                       "M047",
                       "M048",
                       "M049",
                       "M050")

R2roomSensorSet =    ("M030",
                      "M031",
                      "M032",
                      "M033",
                      "M034",
                      "M035",
                      "M036")


upstairsHallSensorSet =    ("M027",
                            "M028",
                            "M029")

downstairsHallSensorSet =    ("M021",
                              "M022",
                              "M023",
                              "M024",
                              "M025",
                              "M026")

kitchenSensorSet =   ("M016",
                      "M017",
                      "M018",
                      "M051" )

bathroomSensorSet =   ("M037",
                       "M038",
                       "M039",
                       "M040",
                       "M041")


labelSet = ("LivRoom",
            "R1room",
            "R2room",
            "UpstairsHall",
            "DownstairsHall",
            "Kitchen",
            "Bathroom",
            "R1room_Light",
            "R3room_Light",
            "uHall_Light",
            "R2room_Light",
            "BA_sink_Light",
            "BA_tub_Light",
            "BA_fan",
            "Liv_Light",
            "dHall_Light",
            "Kitchen_Light")

labelTestSet = ("Kitchen_Light",
                "R1room",
                "R2room",
                "Liv_Light",
                "dHall_Light")

basketsKeySet = ("00", "01", "02", 

                 "10", "11", "12", 

                 "20", "21", "22", 

                 "30", "31", "32", 

                 "40", "41", "42", 

                 "50", "51", "52", 

                 "60", "61", "62")
                

sensorGroupList = [  LivingRoomSensorSet,
                     R1roomSensorSet,
                     R2roomSensorSet,
                     upstairsHallSensorSet,
                     downstairsHallSensorSet,
                     kitchenSensorSet,
                     bathroomSensorSet]




"""
Function sensorFilter
this funcntion will read in the sensor ID and return the primary ID of each group
primary ID for each group is the frist element of that group
"""
def sensorFilter(sensorID):
    for element in sensorGroupList:
            if (element.count(sensorID) > 0):
                return labelSet[sensorGroupList.index(element)]
    if sensorID in lightningMap.keys():
        return lightningMap.get(sensorID)
    return None #return None if not found in the group list




def timeInRange(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
    
def timeInPartition(x):
    for (key) in timePartitionMap:
        if (timeInRange(timePartitionMap[key]["start"],
            timePartitionMap[key]["end"], x)):
            return int(key)
        
def timeStampDiff (timeStamp1, timeStamp2):
    """ Return the absolute different between two timeStamps"""
    #a timeStamp has this format HH:MM:SS:mmmmmmm
    time1 = timeStamp1.split(':')
    time2 = timeStamp2.split(':')
    return abs((float(time1[0])*60 + float(time1[1]) + float(time1[2])*(1/60)) - (float(time2[0])*60 + float(time2[1]) + float(time2[2])*(1/60)))
