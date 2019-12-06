import json
import pandas as pd
import ast
import time
class myDataBase:
    dataFrame=pd.DataFrame()
    def getDataOne(self):
        f = open('../state/data/flightdata2.txt')
        dataStr = ""
        for line in f:
            dataStr += line
        data = json.loads(dataStr)
        aflightno = []
        dflightno = []
        flightnum = []
        atime = []
        dtime = []
        mdl=[]
        dataFrame = pd.DataFrame(columns=["aflightno", "dflightno", "flightnum", "atime", "dtime","mdl"])
        for everyJson in data:
            aflightno.append(everyJson["flightNumber"])
            dflightno.append(everyJson["flightNumberDep"])
            flightnum.append(everyJson["planeNumber"])
            mdl.append(everyJson["flightType"])
            atime.append(pd._libs.tslibs.Timestamp(everyJson["arriveTime"]))
            dtime.append(pd._libs.tslibs.Timestamp(everyJson["leaveTime"]))
        dataFrame["aflightno"] = pd.Series(aflightno)
        dataFrame["dflightno"] = pd.Series(dflightno)
        dataFrame["flightnum"] = pd.Series(flightnum)
        dataFrame["atime"] = pd.Series(atime)
        dataFrame["dtime"] = pd.Series(dtime)
        dataFrame["mdl"] = pd.Series(mdl)


        dataFrame =dataFrame.dropna(subset=["aflightno", "atime", "dtime"])
        dataFrame=dataFrame [dataFrame ["atime"] > pd._libs.tslibs.Timestamp("2019-10-07 00:00:00")]
        dataFrame =dataFrame.sort_values(by=["atime"]).reset_index(drop=True)
        # dataFrame.to_csv("../state/data/dataOne.csv")
        return dataFrame

    def getTypeOfNation(self,x, list):
        if x in list:
            return 1
        else:
            return 0
    def getDataTwo(self):
        # 这里是高峰期数据
        internationalTitle = ["QW", "EU", "CF", "A6", "UW", "O3", "QV", "FD", "UL"]
        # dataIn0602=pd.read_csv("../state/data/0602ad-csv.csv",encoding="utf-8")
        dataFrame= pd.read_csv("../state/data/0603ad-csv.csv", encoding="utf-8")
        # dataIn0603.append(dataIn0602)
        # 将时间搞成正经格式
        dataFrame["atime"] =dataFrame["atime"].apply(
            lambda x: pd._libs.tslibs.Timestamp("2018-06-" + x[-3:-1] + " " + x[0:2] + ":" + x[2:4] + ":00"))
        dataFrame["dtime"] = dataFrame["dtime"].apply(
            lambda x: pd._libs.tslibs.Timestamp("2018-06-" + x[-3:-1] + " " + x[0:2] + ":" + x[2:4] + ":00"))
        # dataIn0603=dataFrame.iloc[0:150]
        dataFrame= dataFrame.loc[(dataFrame["atime"] > pd._libs.tslibs.Timestamp("2018-06-03 00:00:00"))]
        dataFrame= dataFrame.sort_values(by=["atime"]).reset_index(drop=True)
        dataFrame["nation"] = dataFrame["aflightno"].apply(lambda x: self.getTypeOfNation(x[:-4], internationalTitle))
        return dataFrame
    def getDataThree(self):
        f = open('../state/data/flightdatanew.txt')
        dataStr = ""
        for line in f:
            dataStr += line
        data = json.loads(dataStr)
        aflightno = []
        dflightno = []
        flightnum = []
        atime = []
        dtime = []
        mdl=[]
        apassenger=[]
        dpassenger=[]
        nation=[]
        dataFrame = pd.DataFrame(columns=["aflightno", "dflightno", "flightnum", "atime", "dtime","mdl","apassenger","dpassenger","nation"])
        for everyJson in data:
            aflightno.append(everyJson["flightNumber"])
            dflightno.append(everyJson["flightNumberDep"])
            flightnum.append(everyJson["planeNumber"])
            mdl.append(everyJson["mdl"])
            atime.append(pd._libs.tslibs.Timestamp(everyJson["arriveTime"]))
            dtime.append(pd._libs.tslibs.Timestamp(everyJson["leaveTime"]))
            apassenger.append(int(everyJson["arrivepeople"]))
            dpassenger.append(int(everyJson["leavepeople"]))
            nation.append(0 if everyJson["nation"] in ["D","D/D"] else 1)
        dataFrame["aflightno"] = pd.Series(aflightno)
        dataFrame["dflightno"] = pd.Series(dflightno)
        dataFrame["flightnum"] = pd.Series(flightnum)
        dataFrame["atime"] = pd.Series(atime)
        dataFrame["dtime"] = pd.Series(dtime)
        dataFrame["mdl"] = pd.Series(mdl)
        dataFrame["apassenger"] = pd.Series(apassenger)
        dataFrame["dpassenger"] = pd.Series(dpassenger)
        dataFrame["nation"] = pd.Series(nation)


        dataFrame =dataFrame.dropna(subset=["aflightno", "atime", "dtime"])
        dataFrame=dataFrame.loc[dataFrame ["atime"] > pd._libs.tslibs.Timestamp("2019-11-19 05:00:00")]
        dataFrame =dataFrame.sort_values(by=["atime"]).reset_index(drop=True)
        # dataFrame.to_csv("../state/data/dataOne.csv")
        return dataFrame
    def getPossibleOne(self):
        possible = pd.read_json("../state/data/possibleOne.json")
        result = possible["combination"].to_list()
        return result
    def getPossibleTwo(self):
        possible = pd.read_json("../state/data/possibleTwo.json")
        result=possible["combination"].to_list()
        return result
    def gateInf(self):
        nearPosition = pd.read_csv("../state/data/gate-csv.csv", encoding="gbk")
        nationalGateID = nearPosition.loc[(nearPosition["bridge"] == 1) & ((nearPosition["nation"] == "国内"))]
        internationalGateID = nearPosition.loc[(nearPosition["bridge"] == 1) & ((nearPosition["nation"] == "国际"))]
        return nationalGateID,internationalGateID,nearPosition
    def putDataIntoBrowerJson(self,gatePlanDict,typeOfplan,nationOfPlan,atimList,dtimList,numberOfPlan,allGate):
        # 把gatePlanDict转化为前端页面需要的格式
        dataInBrow = {}
        parkingApron = {}
        parkingApron["dimensions"] = ["Name", "Type", "Near Bridge"]
        dataInParkingApron = []
        dataInFlight = []
        minKey=min([int(i) for i in gatePlanDict.keys()])
        for key in sorted(list(gatePlanDict.keys())):
            thisPlan = gatePlanDict[key]
            for plan in thisPlan:
                arriveTime = time.mktime(time.strptime(str(atimList[plan]), "%Y-%m-%d %H:%M:%S"))
                dpartTime = time.mktime(time.strptime(str(dtimList[plan]), "%Y-%m-%d %H:%M:%S"))
                thisData = [int(key)-minKey, int(arriveTime*1000), int(dpartTime*1000), numberOfPlan[plan]+"("+str(typeOfplan[plan])+"|"+str("NAT" if nationOfPlan[plan]==0 else "INT")+")", False, "XX", "XX", "XX", "XX",
                            int(arriveTime*1000)]
                dataInFlight.append(thisData)
            dataInParkingApron.append([key, allGate[allGate["gateno"] == key]["mdl"].iloc()[0] +
                                       "|"+("INT" if allGate[allGate["gateno"] == key]["nation"].iloc()[0]=="国际" else "NAT"), True])
        parkingApron["data"] = dataInParkingApron
        flight = {}
        flight["dimensions"] = ["Parking Apron Index", "Arrival Time", "Departure Time", "Flight Number", "VIP",
                                "Arrival Company", "Departure Company", "Arrival Line", "Departure Line", "Report Time"]
        flight["data"] = dataInFlight
        dataInBrow["parkingApron"] = parkingApron
        dataInBrow["flight"] = flight

        with open("../state/data/dataInBrowser.json","w") as f:
            json.dump(dataInBrow,f)