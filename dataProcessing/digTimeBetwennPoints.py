from dataProcessing import service
from dataProcessing import showData
from dataProcessing import utils
import copy
import pandas as pd
import numpy as np
import datetime
import json
# 这里选的是4月跟5月的数据集
# oneCarRouts=service.getData("oneCarRouts",carId='2',startTime='2019-05-05 15:00:00',endTime='2019-05-05 18:00:00')
# 在浏览器里显示点的信息
# showData.showInBrow(oneCarRouts,infor="gps_time",template="lineTemplate")
startTime=datetime.datetime.now()
shuttlBus=service.getData("shuttlBus")
boardingGate=service.getData("boarding_num")
gateNum=service.getData("gateNum")
parkingPoint=service.getData("parkPoint")


# 防止操作数据过程中修改元数据,将经纬度化为弧度，方便后续的计算
gateNumCopy=copy.deepcopy(gateNum)
gateNumCopy["lng"] = gateNumCopy["lng"].apply(np.math.radians)
gateNumCopy["lat"] = gateNumCopy["lat"].apply(np.math.radians)
boardingGateCopy=copy.deepcopy(boardingGate)
boardingGateCopy["lng"]=boardingGateCopy["lng"].apply(np.math.radians)
boardingGateCopy["lat"]=boardingGateCopy["lat"].apply(np.math.radians)
parkingPointCopy=copy.deepcopy(parkingPoint)
parkingPointCopy["lng"]=parkingPointCopy["lng"].apply(np.math.radians)
parkingPointCopy["lat"]=parkingPointCopy["lat"].apply(np.math.radians)


pathDict={}
for index,bus in shuttlBus.iterrows():
    thisVehicle=bus["vehicle_﻿id"]
    thisCarRouts=service.getData("oneCarRouts",carId=thisVehicle,startTime='2019-04-01 00:00:00',endTime='2019-06-01 00:00:00')
    recorder=[]
    for index1,carRouts in thisCarRouts.iterrows():
        #开始判断入栈元素
        lenRecorder=len(recorder)
        if(lenRecorder==1 and carRouts["speed"]=="0"):
            # 整理数据，清空recorder
            recorder=[]
            continue
        elif(lenRecorder>1 and carRouts["speed"]=="0"):
            pathDict=utils.getPathDict(pathDict,recorder)
            recorder=[]
            continue
        distanceGate =utils.geodistance(gateNumCopy,carRouts["lng"],carRouts["lat"])  # 地球平均半径，6371km
        gateNum["distance"]=distanceGate
        distanceBoading=utils.geodistance(boardingGateCopy,carRouts["lng"],carRouts["lat"])
        boardingGate["distance"]=distanceBoading
        distanceParking=utils.geodistance(parkingPointCopy,carRouts["lng"],carRouts["lat"])
        parkingPoint["distance"]=distanceParking
        # 距离限制
        pointGate=gateNum[gateNum["distance"]<50]["jwbh"]
        pointBoarding=boardingGate[boardingGate["distance"]<25]["bnum"]

        pointParking=parkingPoint[parkingPoint["distance"]<50]["parking_point"]
        if(len(pointGate)>0):
            recorder.append([pointGate.get_values()[0],carRouts["gps_time"]])
            # 防止真的有跟登机口和远机位都很近的点，这种情况理论上不可能
            continue
        elif(len(pointBoarding)>0):
            recorder.append([pointBoarding.get_values()[0], carRouts["gps_time"]])

            continue
        elif(len(pointParking)>0):
            recorder.append([pointParking.get_values()[0],carRouts["gps_time"]])


endTime=datetime.datetime.now()
print("程序用时：",endTime-startTime)
# 数据存入json
jsonPathDict=json.dumps(pathDict)
f=open("pathDict.json","w")
f.write(jsonPathDict)
f.close()
# 数据存入数据库
dataFrameData=pd.DataFrame(columns=["start_point","end_point","time"])
with open("pathDict.json","r") as mydata:
    mydata=json.load(mydata)
dataList=[[],[],[]]
for key in mydata.keys():
    keySplit=key.split("-")
    dataList[0].append(keySplit[0])
    dataList[1].append(keySplit[1])
    dataList[2].append(str(mydata[key]))
dataFrameData["start_point"]=pd.Series(dataList[0])
dataFrameData["end_point"]=pd.Series(dataList[1])
dataFrameData["time"]=pd.Series(dataList[2])
service.putData("time_spend",dataFrameData)