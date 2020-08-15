# -*- coding: utf-8 -*-

timePartitionMap = {"0": {"start": 6, "end": 11}, # Morning
                    "1": {"start": 12, "end": 19}, # Afternoon
                    "2": {"start": 20, "end": 5}} # Everning

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