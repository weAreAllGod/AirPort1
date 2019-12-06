# -*-utf-8-*-
import pandas as pd
import requests
import time
import json

city="昆明"
cityAndCode=pd.read_csv("../state/data/anlysisForDelay/cityAndCode.csv",encoding="gbk")
cityCode=cityAndCode.loc[cityAndCode["district"]==city]["code"].iloc[0]
begin=pd._libs.Timestamp("2018-01-01 00:00:00")-pd._libs.Timedelta("1 days 00:00:00")
tempList=dict()
for i in range(380):
    if i<200:
        begin = begin + pd._libs.Timedelta("1 days 00:00:00")

        url = "http://api.k780.com:88/?app=weather.history&weaid=%s&date=%s&appkey=45909&sign=c8f66ad6b0563d998ac1cb9eecc28bad&format=json" % (cityCode,
        str(begin)[:10])
        weatherData = requests.get(url)
        time.sleep(1)
        backList = []
        if weatherData.json()["success"] == "1":
            weatherDataList = weatherData.json()["result"]
            backList.append(weatherDataList)
            print(weatherDataList)
            tempList[str(begin)[:10]] = weatherDataList
        else:
            tempList[str(begin)[:10]] = []
        print(i)
    else:
        begin = begin + pd._libs.Timedelta("1 days 00:00:00")
        url="http://api.k780.com/?app=weather.history&weaid=%s&date=%s&appkey=45925&sign=480e4217be1f2992f5a3b085db2cd4ae&format=json"%(cityCode,str(begin)[:10])
        weatherData = requests.get(url)
        time.sleep(1)
        backList=[]
        if weatherData.json()["success"]=="1":
            weatherDataList = weatherData.json()["result"]
            backList.append(weatherDataList)
            print(weatherDataList)
            tempList[str(begin)[:10]]=weatherDataList
        else:
            tempList[str(begin)[:10]] = []
        print(i)
with open("%s2.json"%(city),"w") as myfile:
    myfile.write(str(tempList))

