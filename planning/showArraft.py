from dataProcessing import service
from  planning import myFunctions
import pandas as pd
import math
import json
import datetime
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
# 计划到港时间
# arraftFstaData=service.getData("arraft_fsta",startTime='2019-06-08 00:00:00',endTime='2019-06-09 00:00:00')
# arraftFstaData.plot()
# 接口数据，发现不好用
# f=open("../state/data/gatedata.txt")
# objectText=f.readlines()
# jsonText=json.loads(objectText[0])
# dataFrameList=[]
# for jt in jsonText:
#     dataFrameList.append([jt["Airpt_No"],pd._libs.tslibs.timestamps.Timestamp(jt["Schd_Arrv_Dt"]),pd._libs.tslibs.timestamps.Timestamp(jt["Estmt_Dpt_Dt"])])
# dataFrameText=pd.DataFrame(dataFrameList,columns=["Airpt_No","Schd_Arrv_Dt","Estmt_Dpt_Dt"])
# dataAfterOrder=dataFrameText.dropna(subset=["Airpt_No","Schd_Arrv_Dt","Estmt_Dpt_Dt"]).drop_duplicates(subset=["Airpt_No"]).sort_values(by=["Schd_Arrv_Dt"],ascending=True)
# print(dataAfterOrder)



def showFinalResult(mydata, finllGateSort, atimList, dtimList):
    for ylabel, gate in enumerate(finllGateSort):
        for plane in gate:
            allSeconds = int((dtimList[plane] - atimList[plane]).total_seconds())
            if allSeconds > 0:
                plt.plot(pd.date_range(start=atimList[plane], end=dtimList[plane], periods=allSeconds),
                         [ylabel for i in range(allSeconds)], linewidth=3.5)
                plt.text(atimList[plane], ylabel - 0.3, mydata["aflightno"].iloc[plane], fontsize=7)
            else:
                print("有错数据")
                plt.plot(pd.date_range(start=dtimList[plane], end=atimList[plane], periods=np.abs(allSeconds)),
                         [ylabel for i in range(-allSeconds)], linewidth=3.5)
                plt.text(atimList[plane], ylabel - 0.3, "wrongData", fontsize=7)


def showArraftFlight(mydata, atimList, dtimList):
    for i in range(len(atimList)):
        allSeconds = int((dtimList[i] - atimList[i]).total_seconds())
        if allSeconds > 0:
            plt.plot(pd.date_range(start=atimList[i], end=dtimList[i], periods=allSeconds),
                     [i for j in range(allSeconds)], linewidth=2)
            plt.text(atimList[i], i, mydata["aflightno"].iloc[i], fontsize=4)

if __name__ == '__main__':

    # 这里用去年学姐的数据
    dataIn0603=pd.read_csv("../state/data/0603ad-csv.csv",encoding="utf-8")
    # 将时间搞成正经格式

    dataIn0603["atime"]=dataIn0603["atime"].apply(lambda x:pd._libs.tslibs.Timestamp("2018-06-"+x[-3:-1]+" "+x[0:2]+":"+x[2:4]+":00") )
    dataIn0603["dtime"]=dataIn0603["dtime"].apply(lambda x:pd._libs.tslibs.Timestamp("2018-06-"+x[-3:-1]+" "+x[0:2]+":"+x[2:4]+":00") )
    dataIn0603=dataIn0603[dataIn0603["atime"]>pd._libs.tslibs.Timestamp("2018-06-03 00:00:00")]
    dataIn0603=dataIn0603.sort_values(by=["atime"]).reset_index(drop=True)
    # 也可以用loc
    atimList=dataIn0603["atime"].to_list()
    dtimList=dataIn0603["dtime"].to_list()
    lenAtimeList=len(atimList)
    conflictDict=dict()
    for i in range(lenAtimeList):
        tempList = []
        for j in range(i+1,lenAtimeList):
            if atimList[j]-dtimList[i]<pd.Timedelta("0 days 00:20:00"):
                tempList.append(j)
            else:
                if tempList==[]:
                    break
                else:
                    conflictDict[i] = tempList
                    break
    # thisProB=[[-1, -5], [[-1, 1], [5, 6]], [2, 30], [[0, 0]], [0], [[(0, 4), (0, None)]]]
    # 机位的信息
    gateInfor=pd.read_csv("../state/data/gate-csv.csv",encoding="gbk")

    assignment=[]
    thisPlaneNumber=0
    for plane in dataIn0603.iterrows():
        door=True
        maxTime=pd._libs.tslibs.Timestamp("2018-01-01 00:00:00")
        for index, everyAss  in enumerate(assignment):
            if len(everyAss)!=0 and plane[1]["atime"]-everyAss[-1][-1]>pd.Timedelta("0 days 00:20:00") and everyAss[-1][-1]>maxTime:
                door=False
                maxIndex = index
                maxTime=everyAss[-1][-1]

                # everyAss.append([plane[1]["atime"],plane[1]["dtime"]])
                # break
        if door:
            assignment.append([[thisPlaneNumber,plane[1]["atime"],plane[1]["dtime"]]])
            thisPlaneNumber+=1
        else:
            assignment[maxIndex].append([thisPlaneNumber,plane[1]["atime"],plane[1]["dtime"]])
            thisPlaneNumber+=1
    numberOfPlane=[len(i) for i in assignment]
    assignmentDataFrame=pd.DataFrame(pd.Series(numberOfPlane),columns=["numberOfPlane"])
    # assignmentDataFrame=assignmentDataFrame.sort_values(by=["numberOfPlane"],ascending=False)
    yLabel=1
    for item in assignmentDataFrame.iterrows():
        for everyPlane in assignment[item[0]]:
            allSeconds=int((everyPlane[-1] - everyPlane[-2]).total_seconds())
            plt.plot(pd.date_range(start=everyPlane[-2],end=everyPlane[-1],periods=allSeconds),[yLabel for i in range(allSeconds)])
        yLabel+=1



    # for index,gate in enumerate(assignment):
    #     for everyPlane in gate:
    #         allSeconds=int((everyPlane[-1] - everyPlane[-2]).total_seconds())
    #         plt.plot(pd.date_range(start=everyPlane[-2],end=everyPlane[-1],periods=allSeconds),[index for i in range(allSeconds)])














    #
    # m,n=lenAtimeList,gateInfor.shape[0]
    # bridges=[gate[1]["bridge"] for gate in gateInfor.iterrows()]
    # cc=[bridges[int(math.fmod(i,n))] for i in range(m*n)]
    # # 不等式约束
    # Aub=None
    # bub=None
    # # 等式约束
    # Aeb=[]
    # for j in range(m):
    #     tempList=[]
    #     for i in range(n*m):
    #         if i <(j+1)*n and i>=j*n:
    #             tempList.append(1)
    #         else:
    #             tempList.append(0)
    #     Aeb.append(tempList)
    #
    # beb=[1 for i in range(m)]
    # boundary=[[(0,1) for i in range(m*n)]]
    #
    # thisPro=[cc,Aub,bub,Aeb,beb,boundary]
    # mySolver=myFunctions.solver()
    # allResults=mySolver.branchDelimitation(thisPro)
    # 变量个数m*n



