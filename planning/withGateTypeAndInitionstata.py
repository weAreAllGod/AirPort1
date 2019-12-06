import numpy as np
from pandas.plotting import register_matplotlib_converters
from tools import funcForColumn
from tools.cplexFunc import cplexSoverMain,cplexForSecondPro
from tools.dataBase import myDataBase
import pandas as pd
import datetime
from tools import printResult
import time
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
    initalData,data = dataBase.getDataThree()
    ##对于初始航班只关心停在近机位的,近机位从101到169
    initalData=initalData.loc[initalData["parkinggate"].isin(range(101,169))]
    data=data.iloc[:150,:]
    #表示前lenInitalData的条件取等
    lenInitalData=len(initalData)
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
    #总的数据
    data=pd.concat([initalData, data]).reset_index(drop=True)
    #去除过夜的后
    # mydata = data.loc[data["dtime"]<(pd.Timestamp(str(minAtime)[:10]+" 00:00:00")+pd.Timedelta("1 days"))]
    # 将初始条件合并到要分配的航班中去

    mydata=data.sort_values(by=["atime"]).reset_index(drop=True)
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
    beginTime = datetime.datetime.now()
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

    # 每个变量所属的类型以及国际国内航班属性
    typeOfParas=[]
    nationOfParas=[]
    for everyPara in possibles:
        typeOfParas.append(max([numberOfTypeForPlan[i] for i in everyPara]))
        nationOfParas.append(max([nationOfPlan[i] for i in everyPara]))
    # 国际F只能停国际F的飞机，国际E可以停国际E和F,国际D可以停国际E,F,D.国际C,可以停C,D,E,F。
    #（总共8个条件,再加上初始条件，有几个就加几个条件总共lenInitalData） 国内F可以停国内F和国际F,国内E可以停国内E,F和国际E,F,国内D可以停国内D,E,F以及国际的D,E,F,国内C，可以停国内C,D,E,F和国际的C,D,E,F
    reMatrix = np.zeros((len(atimList) + 8+lenInitalData, len(possibles)))
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

    '''
    这里的理解和下标问题太容易出错了
    '''
    # 中间加上lenInitalData的约束
    for j in range(lenInitalData):
        for jj in range(reMatrix.shape[1]):
            #从第8行开始写
            reMatrix[8+j,jj]=1 if j in possibles[jj] else 0
    # 后面飞机的约束
    for i1 in range(lenInitalData,len(atimList)):
        for ii in range(reMatrix.shape[1]):
            reMatrix[i1+8, ii] = 1 if i1 in possibles[ii] else 0



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


    # 约束的等号
    my_sense = ""
    for i in range(8):
        my_sense += 'L'
    for j in range(8,8+lenInitalData):
        my_sense+="E"
    for j1 in range(8+lenInitalData,8+lenInitalData+len(atimList)):
        my_sense+="L"

    print("矩阵数据准备完毕", datetime.datetime.now() - beginTime)
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
    my_prob = cplexSoverMain(c, reMatrix, b, "I",my_sense)
    my_prob.write("../state/data/problem.lp")
    my_prob.solution.write("../state/data/result.lp")
    x = my_prob.solution.get_values()
    print("Solution value  = ", my_prob.solution.get_objective_value())
    print('result: ')
    result = [possibles[index] for index, value in enumerate(x) if value == 1]
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
    printResult.gateToPlan(gatePlanDict, atimList, dtimList, numberOfPlan, nationOfPlan, typeOfplan, allGate)
    gatePlanDict2=funcForColumn.gateToPlanMethodsTwo(allGate,result,resultInf,atimList,dtimList,nationOfResult,typeOfResult)
    print("------------------------贪心法计算结果--------------------->")

    printResult.gateToPlan(gatePlanDict2, atimList, dtimList, numberOfPlan, nationOfPlan, typeOfplan, allGate)


    dataBase.putDataIntoBrowerJson(gatePlanDict2,typeOfplan,nationOfPlan,atimList,dtimList,numberOfPlan,allGate)
    printResult.analysisOfPlans(result, data, dataNearByHum, resultInf, atimList)












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







