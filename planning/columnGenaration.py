import numpy as np
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
register_matplotlib_converters()
from tools.funcForColumn import  treeNote, searcher2,gateSearcher,gateNode,getConflictFlight
from tools.cplexFunc import cplexSoverMain
from tools.dataBase import myDataBase
import pandas as pd
import datetime
def showFinalResult(mydata,finllGateSort,atimList,dtimList):
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

def showArraftFlight(mydata,atimList,dtimList):
    for i in range(len(atimList)):
        allSeconds = int((dtimList[i] - atimList[i]).total_seconds())
        if allSeconds > 0:
            plt.plot(pd.date_range(start=atimList[i], end=dtimList[i], periods=allSeconds),
                     [i for j in range(allSeconds)], linewidth=2)
            plt.text(atimList[i], i, mydata["aflightno"].iloc[i], fontsize=4)

if __name__ == '__main__':

    # 基础数据
    dataBase=myDataBase()
    data=dataBase.getDataTwo()
    ##对国际和国内航班进行统计
    #航班号以这几个开头的为国际[QW,EU,CF,A6, UW,O3,QV,FD,UL]
    internationalTitle=["QW","EU","CF","A6", "UW","O3","QV","FD","UL"]
    data["nation"]=data["aflightno"].apply(lambda x:x[:-4])
    internationalPlantData=data.loc[data["nation"].isin(internationalTitle ) ]
    nationalPlantData=data.loc[~data["nation"].isin(internationalTitle) ]
    # 国内航班停机位27,国际航班停机位38
    bridgeNumber=65
    mydata=data
    atimList=mydata["atime"].to_list()
    dtimList=mydata["dtime"].to_list()
    beginTime=datetime.datetime.now()



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
    # possibles = searcher2(listNodes)

    # listNodes = []
    # lenAtimeList = len(atimList)
    # result=[]
    # for i in range(lenAtimeList):
    #     thisDtime = dtimList[i]
    #     thisList = []
    #     for j in range(i + 1, lenAtimeList):
    #         if atimList[j] - thisDtime < pd.Timedelta("0 days 00:20:00") or dtimList[j]-dtimList[i] < pd.Timedelta("0 days 00:20:00") or dtimList[j] - atimList[i] < pd.Timedelta("0 days 00:20:00") or atimList[j]-atimList[i] <pd.Timedelta("0 days 00:20:00") :
    #             thisList.append(j)
    #     result.append(thisList)
        # thisNode = treeNote(i, thisList)
        # listNodes.append(thisNode)

    possibles=dataBase.getPossibleTwo()
    reMatrix=np.zeros((len(atimList)+1,len(possibles)))
    # 近机位约束
    reMatrix[0,:]=1
    for i in range(len(atimList)):
        for j, possible in enumerate(possibles):
            if i in possible:
                reMatrix[i+1,j]=1
    print("矩阵数据准备完毕",datetime.datetime.now()-beginTime)
    #这里是靠桥的c
    c=[len(i) for i in  possibles]
    #这里是靠桥人数的c
    passengers=[]
    for flt in mydata.iterrows():
        passengers.append(flt[1]["apassenger"]+flt[1]["dpassenger"])
    pc=[]
    for fa in possibles:
        totalNumer=0
        for i in fa:
            totalNumer+=passengers[i]
        pc.append(totalNumer)
    b=[1 for i in range(reMatrix.shape[0])]
    b[0]=65
    my_prob=cplexSoverMain(pc,reMatrix,b,"I")
    my_prob.write("../state/data/problem.lp")
    my_prob.solution.write("../state/data/result.lp")
    print("Solution value  = ", my_prob.solution.get_objective_value())
    x = my_prob.solution.get_values()
    result=[possibles[index] for index,value in enumerate(x) if value==1]
    print('result: ')
    print(result)
    ##如果分配的结果小于65说明所有的都可以靠桥，将result补满
    if len(result)<bridgeNumber:
        for i in range(bridgeNumber-len(result)):
            result.append([])
    ##接下来根据出入时间不能小于20分钟进行机位排序
    conflictTime=[[atimList[flight] for flight in gate]+[dtimList[flight] for flight in gate]  for gate in result]
    conflictTimeList=[]
    for index1,value1 in enumerate(conflictTime):
        thisConflicts=[]
        for index2,value2 in enumerate(conflictTime):
            if getConflictFlight(value1,value2):
                continue
            else:
                thisConflicts.append(index2)
        newGate=gateNode(index1,thisConflicts)
        conflictTimeList.append(newGate)
    print("不冲突矩阵")
    for gateNode in conflictTimeList:
        print(gateNode.value,gateNode.noConflicts)
    gateS=gateSearcher()
    print("排序结果")
    finallR=[]
    for i in range(bridgeNumber):
        gateS.finallyResult=[]
        for node in conflictTimeList:
            node.myPointer=0
        gateS.searchGateNode(conflictTimeList,conflictTimeList[i],[])
        print("%s最终分配的长度"%i)
        print( len(gateS.finallyResult))
        if  len(gateS.finallyResult)==bridgeNumber:
            finallR=gateS.finallyResult
            print("得到最终结果：")
            print(gateS.finallyResult)
            break
        elif(len(gateS.finallyResult)>len(finallR)):
            finallR=gateS.finallyResult
            ##未被分配

        # 这里进行后续的优化操作
        notBeChoosed = set(range(len(result))).difference(finallR)
        for thisNotBe in notBeChoosed:
            for i in range(len(finallR) - 1):
                if (i == 0) and (thisNotBe in conflictTimeList[i].noConflicts):
                    finallR.insert(i, thisNotBe)
                elif (i != 0 and (thisNotBe in conflictTimeList[i].noConflicts)) and (
                        thisNotBe in conflictTimeList[i + 1].noConflicts):
                    finallR.insert(i, thisNotBe)
                    break
        if (len(finallR) == bridgeNumber):
            print("得到全局最优解：")
            print(finallR)
            break
        else:
            print("有%s个机位进出存在冲突。" % (bridgeNumber - len(finallR)))

    print("靠桥率：",sum([len(item) for item in result])/len(atimList))
    ###展示分配结果
    finllGateSort=[result[gate] for gate in finallR]
    showFinalResult(mydata,finllGateSort,atimList,dtimList)
    # 深度遍历
    # maxLenRout=[]
    # testRout = [conflictTimeList[0]]
    # while True:
    #     lastNode=testRout[-1]
    #     if lastNode.myPointer<lastNode.getUpBound():
    #         childOfLast=conflictTimeList[lastNode.noConflicts[lastNode.myPointer]]
    #         lastNode.myPointer+=1
    #         if childOfLast not in testRout:
    #             testRout.append(childOfLast)
    #             if len(testRout)>len(maxLenRout):
    #                 maxLenRout=testRout
    #                 if len(maxLenRout)==65:
    #                     print("得到最终结果")
    #                     print(maxLenRout)
    #                     break
    #             printValue=[r.value for r in testRout]
    #             print(printValue)
    #         else:
    #             continue
    #     else:
    #         testRout.pop()
    #         if len(testRout)==0 :
    #             print("遍历完毕，没有找到结果")
    #             break
    #         lastNode.myPointer=0

