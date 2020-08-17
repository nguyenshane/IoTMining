# -*- coding: utf-8 -*-

timePartitionMap = {"0": {"start": 6, "end": 11}, # Morning
                    "1": {"start": 12, "end": 19}, # Afternoon
                    "2": {"start": 20, "end": 5}} # Everning

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
                return element[0]
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
    return abs((int(time1[0])*60 + int(time1[1])) - (int(time2[0])*60 + int(time2[1])))

