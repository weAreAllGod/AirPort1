from math import radians, cos, sin, asin, sqrt
import numpy as np
def geodistance(date,lng2,lat2):
    """

    :param date:
    :param lng2:
    :param lat2:
    :return: 计算两者之间的距离，返回的是一个pandas.Series对象
    """

    lng2 = radians(float(lng2))
    lat2 = radians(float(lat2))
    dlon = date["lng"] - lng2
    dlat = date["lat"] - lat2
    a = np.sin(dlat / 2) ** 2 + np.cos(date["lat"]) * cos(lat2) * np.sin(dlon / 2) ** 2
    # 得到的是米
    distance = 2 * a.apply(np.math.sqrt).apply(np.math.asin) * 6371 * 1000  #
    return distance

def getPathDict(pathDict,recorder):
    lenRecorder=len(recorder)
    for index1 in range(lenRecorder):
        recor1 = recorder[index1]
        for index2 in range(index1, lenRecorder):
            recor2 = recorder[index2]
            tempKey = str(recor1[0]) + "-" + str(recor2[0])
            thisValue = (recor2[1] - recor1[1]).seconds
            # 键值对不存在，创建
            if tempKey not in pathDict.keys():
                pathDict[tempKey] = [thisValue]
                continue
            # 键值对已经存在，并且历史上没有这个值
            elif(thisValue not in pathDict[tempKey]):
                pathDict[tempKey].append(thisValue)
    return pathDict