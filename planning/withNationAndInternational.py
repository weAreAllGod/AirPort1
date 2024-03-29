import numpy as np
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt

register_matplotlib_converters()
from tools import funcForColumn
from tools.cplexFunc import cplexSoverMain,cplexForSecondPro
from tools.dataBase import myDataBase
import pandas as pd
import datetime
from tools import printResult
import time


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
def getTypeOfPosition(x):
    if x=="C":
        return 0
    elif(x=="D"):
        return 1
    elif(x=="E"):
        return 2
    elif(x=="F"):
        return 3
    else:
        return print("在获取机位类型的时候出现了错误")

def getTypeOfNation(x,list):
    if x in list:
        return 1
    else:
        return 0

if __name__ == '__main__':

    dataId = 0#0表示所有的数据，1表示国内的数据，2表示国际的数据
    # 基础数据
    dataBase = myDataBase()
    # data = dataBase.getDataTwo()
    initialData,alldata = dataBase.getDataThree()
    data=alldata.iloc[:120,:]
    ##对国际和国内航班进行统计
    # 航班号以这几个开头的为国际[QW,EU,CF,A6, UW,O3,QV,FD,UL]

    # internationalPlantData = data.loc[data["nation"].isin(internationalTitle)]
    # nationalPlantData = data.loc[~data["nation"].isin(internationalTitle)]
    # 国内航班停机位27,国际航班停机位38
    ##除了互斥时间外，还考虑了近机位数量限制，机位的类型限制,类型包括C,D,E,F四种类型的停机位
    ##近机位C,D,E,F数量[23,34,6,2]
    ##国内近机位C,D,E,F数量[20,27,4,1]
    ##国际近机位C,D,E,F数量[3,7,2,1]
    nationalType=[22, 28, 4, 1]
    internationalType=[3,7,2,1]
    nationalNumber=sum(nationalType)
    internationalNumber =sum(internationalType)
    allNumber = nationalNumber+internationalNumber
    #进行去除过夜航班的操作，过夜航班不放在近机位
    minAtime=data["atime"].min()
    # mydata = data
    mydata = data.loc[data["dtime"]<(pd.Timestamp(str(minAtime)[:10]+" 00:00:00")+pd.Timedelta("1 days"))]
    mydata=mydata.sort_values(by=["atime"]).reset_index(drop=True)
    bridgeNumber = allNumber
    # 人工分配结果
    # dataNearByHum=mydata.loc[mydata["gate"].isin(dataBase.gateInf()[0]["gateno"].to_list())]
    dataNearByHum=[]
    atimList = mydata["atime"].to_list()
    dtimList = mydata["dtime"].to_list()
    numberOfPlan=mydata["aflightno"].to_list()
    typeOfplan=mydata["mdl"].apply(lambda x:x[-1:]).to_list()
    nationOfPlan=mydata["nation"].to_list()
    # 机位类型CDEF分别为0，1，2，3
    numberOfTypeForPlan=mydata["mdl"].apply(lambda x:getTypeOfPosition(x[-1])).to_list()
    # 机位的国际国内类型国内是0，国际是1
    # typeOfNation=mydata["dflightno"].apply(lambda x:getTypeOfNation(x[:-4],internationalTitle)).to_list()
    time1 = datetime.datetime.now()
    listNodes=[]
    lenAtimeList=len(atimList)
    for i in range(lenAtimeList):
        thisDtime=dtimList[i]
        thisList=[]
        for j in range(i+1,lenAtimeList):
            if atimList[j]-thisDtime>pd.Timedelta("0 days 00:20:00"):
                thisList.append(j)
        thisNode=funcForColumn.treeNote(i,thisList)
        listNodes.append(thisNode)

    possibles = funcForColumn.searcher2(listNodes)##里面存放的是所有的变量
    time2 = datetime.datetime.now()
    print("变量构建时间",time2-time1)
    # 每个变量所属的类型以及国际国内航班属性
    typeOfParas=[]
    nationOfParas=[]
    for everyPara in possibles:
        typeOfParas.append(max([numberOfTypeForPlan[i] for i in everyPara]))
        nationOfParas.append(max([nationOfPlan[i] for i in everyPara]))
    # 国际F只能停国际F的飞机，国际E可以停国际E和F,国际D可以停国际E,F,D.国际C,可以停C,D,E,F。
    # 国内F可以停国内F和国际F,国内E可以停国内E,F和国际E,F,国内D可以停国内D,E,F以及国际的D,E,F,国内C，可以停国内C,D,E,F和国际的C,D,E,F
    reMatrix = np.zeros((len(atimList) + 8, len(possibles)))
    #国际F型停机位的限制
    for i in range(reMatrix.shape[1]):
        reMatrix[0,i]=1 if (typeOfParas[i]==3 and nationOfParas[i]==1) else 0
    #国际E型停机位的限制
    for i in range(reMatrix.shape[1]):
        reMatrix[1,i]=1 if (nationOfParas[i]==1 and (typeOfParas[i] in [2,3])) else 0
    #国际D型停机位的限制
    for i in range(reMatrix.shape[1]):
        reMatrix[2, i] = 1 if (nationOfParas[i]==1 and (typeOfParas[i] in [1,2,3]) ) else 0
    #国际C型停机位的限制
    reMatrix[3,:]=nationOfParas

    #国内F型停机位
    for i in range(reMatrix.shape[1]):
        reMatrix[4,i]=1 if (typeOfParas[i]==3) else 0

    # 国内E型停机位
    for i in range(reMatrix.shape[1]):
        reMatrix[5, i] = 1 if (typeOfParas[i] in [2,3]) else 0
    # 国内D型停机位
    for i in range(reMatrix.shape[1]):
        reMatrix[6, i] = 1 if (typeOfParas[i] in [1,2, 3]) else 0
    reMatrix[7,:]=[1 for i in range(reMatrix.shape[1])]

    ##b的设置要与上面对应
    b = [1 for i in range(reMatrix.shape[0])]
    # 对应上面的近机位约束，国际约束，F,E,D型约束，共5各约束
    b[0] = internationalType[3]
    b[1]=sum(internationalType[-2:])
    b[2]=sum(internationalType[-3:])
    b[3]=sum(internationalType)

    b[4]=internationalType[3]+nationalType[3]
    b[5] = sum(internationalType[-2:] + nationalType[-2:])
    b[6] = sum(internationalType[-3:] + nationalType[-3:])
    b[7] = sum(internationalType + nationalType)
    # 符号
    my_sense = ""
    for i in range(len(b)):
        my_sense += 'L'
    for i in range(len(atimList)):
        for j, possible in enumerate(possibles):
            if i in possible:
                reMatrix[i + 8, j] = 1

    # 这里是靠桥的c
    c = [len(i) for i in possibles]
    # 这里是靠桥人数的c
    passengers = []
    for flt in mydata.iterrows():
        passengers.append(flt[1]["apassenger"] + flt[1]["dpassenger"])
    pc = []
    for fa in possibles:
        totalNumer = 0
        for i in fa:
            totalNumer += passengers[i]
        pc.append(totalNumer)
    time3=datetime.datetime.now()
    print("模型构建时间", time3-time2)
    my_prob = cplexSoverMain(c, reMatrix, b, "I",my_sense)
    my_prob.write("../state/data/problem.lp")
    my_prob.solution.write("../state/data/result.lp")
    x = my_prob.solution.get_values()

    print("Solution value  = ", my_prob.solution.get_objective_value())
    print('result: ')
    result = [possibles[index] for index, value in enumerate(x) if value == 1]
    time4 = datetime.datetime.now()
    print("Model1求解时间：",time4-time3)
    indexOfResult=[index for index, value in enumerate(x) if value == 1]
    print(result)
    typeOfResult = [typeOfParas[item] for item in indexOfResult]
    nationOfResult = [nationOfParas[item] for item in indexOfResult]

    resultInf = funcForColumn.anlysisForResult(result, typeOfResult, nationOfResult)
    # hamiltonRouts,notBeChoosed=getHamiltonRouts(conflictTimeList)
    nationalGateInf, internationalGateInf, allGate = dataBase.gateInf()
    # 这里是第一种方法，用n个哈密尔顿通路进行拼接
    gatePlanDict=funcForColumn.getPlanToGate(resultInf,internationalGateInf,nationalGateInf,atimList, dtimList)
    #第二种贪心分配方法
    time5 = datetime.datetime.now()
    printResult.gateToPlan(gatePlanDict, atimList, dtimList, numberOfPlan, nationOfPlan, typeOfplan, allGate)
    gatePlanDict2=funcForColumn.gateToPlanMethodsTwo(allGate,result,resultInf,atimList,dtimList,nationOfResult,typeOfResult)
    time6 = datetime.datetime.now()
    print("Model2求解时间：",time6-time5)
    print("------------------------贪心法计算结果--------------------->")
    printResult.gateToPlan(gatePlanDict2, atimList, dtimList, numberOfPlan, nationOfPlan, typeOfplan, allGate)
    printResult.analysisOfPlans(result, data, dataNearByHum, resultInf, atimList)

    dataBase.putDataIntoBrowerJson(gatePlanDict2,typeOfplan,nationOfPlan,atimList,dtimList,numberOfPlan,allGate)












    """放方案1

    listNodes=[]
    lenAtimeList=len(atimList)
    for i in range(lenAtimeList):
        thisDtime=dtimList[i]
        thisList=[]
        for j in range(i+1,lenAtimeList):
            if atimList[j]-thisDtime>pd.Timedelta("0 days 00:20:00"):
                thisList.append(j)
        thisNode=treeNote(i,thisList)
        listNodes.append(thisNode)
    possibles=searcher.getPossibles(listNodes)
    存为json方便后面处理
    """
    """方案二效率更高一些
    possibles=searcher2(listNodes)
    """

    '''cplex精确求解,经证实该方法在可接受时间内无法给出满意解。
    paraForSecond,boundForSecond=getParasAndBoundForSecondPro(result, nationOfResult, typeOfResult, conflictTimeList)
    my_colnames = []
    for line in range(len(paraForSecond)):
        for column in range(len(paraForSecond)):
            if paraForSecond[line][column] == 1:
                my_colnames.append("y%s,%s" % (line, column))
    secondPro=cplexForSecondPro(paraForSecond,boundForSecond,result)

    '''

    '''
    ##如果分配的结果小于65说明所有的都可以靠桥，将result补满
    if len(result) < bridgeNumber:
        for i in range(bridgeNumber - len(result)):
            result.append([])
    ###结果之间的不冲突关系，用链表的方式存储
    dontConflictTimeList,conflictTimeList=funcForColumn.conflictForResult(atimList,dtimList,result)
    print("不冲突矩阵关系如下：")
    for gateNode in dontConflictTimeList:
        print(gateNode.value, gateNode.noConflicts)
    print("冲突矩阵关系如下:")
    for gateNode in conflictTimeList:
        print(gateNode.value, gateNode.noConflicts)
    
    '''







