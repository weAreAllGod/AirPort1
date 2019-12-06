import dataProcessing
from  dataProcessing import service
from dataProcessing import  showData
import pandas as pd
import requests
import json
import datetime

# 这段代码生成了模板allPointsTemplate
"""
gatePoints=service.getData("gateNum")
boardingPoints=service.getData("boarding_num")
parkingPoints=service.getData("parkPoint")
allPoints=pd.DataFrame(columns=["pointName","lng","lat"])
allPoints.pointName=gatePoints.jwbh.append(boardingPoints.bnum,ignore_index=True).append(parkingPoints.parking_point,ignore_index=True)
allPoints.lng=gatePoints.lng.append(boardingPoints.lng,ignore_index=True).append(parkingPoints.lng,ignore_index=True)
allPoints.lat=gatePoints.lat.append(boardingPoints.lat,ignore_index=True).append(parkingPoints.lat,ignore_index=True)
showData.showInBrow(allPoints,infor="pointName",template="template")

"""
# 生成所有车辆实时展示图

realTimeCars=requests.get("http://119.254.234.117:28080/openapi/carGps")
realTimeCars=realTimeCars.text
jsonRealTimeCars=json.loads(realTimeCars)
carDataFrame=pd.DataFrame(columns=["vehicle_id","plate","lng","lat","gps_time"])
# id对照表
carId=service.getData("car_id")
vehicle_id=[]
plate=[]
lng=[]
lat=[]
gps_time=[]
for car in jsonRealTimeCars:
    vehicle_id.append(car["vehicle_id"])
    plate.append(carId[carId["vehicle_id"]==str(car["vehicle_id"])]["plate"].get_values()[0])
    # print(carId[carId["vehicle_id"]==car["vehicle_id"]]["plate"])
    lng.append(car["lng"])

    lat.append(car["lat"])
    gps_time.append(datetime.datetime.fromtimestamp(car["gps_time"]/1000))#去掉末尾的3个0



carDataFrame["vehicle_id"]=pd.Series(vehicle_id)
carDataFrame["plate"]=pd.Series(plate)
carDataFrame["lng"]=pd.Series(lng).astype("float")
carDataFrame["lat"]=pd.Series(lat).astype("float")
carDataFrame["gps_time"]=pd.Series(gps_time)

# oneCar=carDataFrame[carDataFrame["vehicle_id"]==9]
# oneCar=carDataFrame[carDataFrame["plate"]=="民航D6648" ]
oneCar=carDataFrame
showData.showInBrow(oneCar,infor="vehicleAndTime",template="allPointsTemplate")

# print(oneCar)
# carId=service.getData("car_id")
# for index ,value in carId.iterrows():
#     print("dictionary.set('%s', '%s');"%(value["vehicle_id"],value["plate"]))




# print(jsonRealTimeCars[0])


# oneCarRouts=service.getData("oneCarOnTime",carId="74",startTime="2019-08-08 00:00:00",endTime="2019-08-08 14:00:00")
# print(oneCarRouts)
# showData.showInBrow(oneCarRouts,template="lineTemplate",infor="gps_time")




