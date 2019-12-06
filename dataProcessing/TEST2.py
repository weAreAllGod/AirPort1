import json
import pandas as pd
f=open('../state/data/flightdata.txt')
dataStr=""
for line in f:
    dataStr+=line
data=json.loads(dataStr)
aflightno=[]
dflightno=[]
flightnum=[]
atime=[]
dtime=[]
dataFrame=pd.DataFrame(columns=["aflightno","dflightno","flightnum","atime","dtime"])
for everyJson in data:
    aflightno.append(everyJson["flightNumber"])
    aflightno.append(everyJson["flightNumberDep"])
    flightnum.append(everyJson["planeNumber"])
    atime.append(pd._libs.tslibs.Timestamp(everyJson["arriveTime"]))
    dtime.append(pd._libs.tslibs.Timestamp(everyJson["leaveTime"]))
    print(everyJson)
dataFrame["aflightno"]=pd.Series(aflightno)
dataFrame["dflightno"]=pd.Series(aflightno)
dataFrame["flightnum"]=pd.Series(aflightno)
dataFrame["atime"]=pd.Series(atime)
dataFrame["dtime"]=pd.Series(dtime)
dataFrame=dataFrame.dropna(subset=["aflightno","atime","dtime"])
