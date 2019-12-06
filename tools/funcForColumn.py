import copy
import pandas as pd
from tools.dataBase import myDataBase
class treeNote:
    myPointer=0
    def __init__(self,value,pointers):
        self.value=value
        self.pointers=pointers
    def getValue(self):
        return  self.pointers[self.myPointer]
    def getUpBound(self):
        return len(self.pointers)

class searcher:
    allRouts=[]
    def searchRout(self,tree,thisnode,resultList):
        # 还需要把上一个结点记下来
        thisValue = thisnode.value
        oldResultList = copy.deepcopy(resultList)
        resultList.append(thisValue)
        if thisnode.myPointer<(thisnode.getUpBound()) :
            nextnode = thisnode.pointers[thisnode.myPointer]
            thisnode.myPointer=thisnode.myPointer+1
            self.searchRout(tree,tree[nextnode],resultList)
            if resultList not in self.allRouts:
                self.allRouts.append(resultList)
            else:
                self.allRouts.append(resultList[:-1])
            # for item in tree[thisValue].pointers:
            #     tree[item].myPointer=0
            self.searchRout(tree, tree[thisValue], oldResultList)
    def getPossibles(self,listNodes):
        mySearcher = searcher()
        possibles = []
        for i in range(len(listNodes)):
            mySearcher.searchRout(listNodes, listNodes[i], [])
            allPosiiile = mySearcher.allRouts
            if allPosiiile != []:
                for everyRout in allPosiiile:
                    possibles.append(everyRout)
                    print(everyRout)
                # 该搜索算法，结束时没有根节点，最后把根节点加进去
                possibles.append([i])
            else:
                possibles.append([i])
            mySearcher.allRouts = []
            # 搜索后指针复位
            for node in listNodes:
                node.myPointer = 0
        return possibles


def searcher2(listNodes):
    result=[]
    for i in range(len(listNodes)):
        temprouts = [listNodes[i].value]
        while True:
            lastNode=listNodes[temprouts[-1]]
            if lastNode.myPointer<lastNode.getUpBound():
                nextNode=listNodes[lastNode.pointers[lastNode.myPointer]]
                lastNode.myPointer += 1
                temprouts.append(nextNode.value)
            else:
                result.append(copy.deepcopy(temprouts))
                # print(temprouts)
                temprouts.pop()
                if len(temprouts)==0:
                    break
        for item in listNodes:
            item.myPointer=0
    return result
class gateSearcher:
    finallyResult=[]
    i=0
    maxItem=5
    sentinel=True
    gate=0
    def searchGateNode(self,tree,thisnode,resultList):
        thisValue = thisnode.value
        oldResultList = copy.deepcopy(resultList)
        if thisValue not in resultList:
            resultList.append(thisValue)

        else:
            self.gate=1
        ##将最长分配结果保留
        if len(self.finallyResult)<=len(resultList):
            self.finallyResult=resultList
            self.i=0

        elif(len(self.finallyResult)==len(resultList)):
            self.i+=1

        if len(resultList)==65 or self.i==self.maxItem:
            self.sentinel=False
        if thisnode.myPointer < (thisnode.getUpBound())  and self.sentinel and self.gate==0:
            nextnode = thisnode.noConflicts[thisnode.myPointer]
            thisnode.myPointer = thisnode.myPointer + 1
            self.searchGateNode(tree, tree[nextnode], resultList)
            self.gate=0
            self.searchGateNode(tree, tree[thisValue], oldResultList)

class gateNode:
    myPointer=0
    beVised=[]
    def __init__(self,value,noConflicts):
        self.value=value
        self.noConflicts=noConflicts
    def getUpBound(self):
        return len(self.noConflicts)



def getConflictFlight(flight1,flight2):
    for time1 in flight1:
        # print("----",time1)
        for time2 in flight2:
            if pd.Timedelta("0 days 00:00:00")<=time1-time2<=pd.Timedelta("0 days 00:10:00") or pd.Timedelta("0 days 00:00:00")<=time2-time1<=pd.Timedelta("0 days 00:10:00"):
                # print(time2)
                return True
    return False

def conflictForResult(atimList,dtimList,result):
    ##接下来根据出入时间不能小于20分钟进行机位排序
    if len(result)==0 or len(result)==1:
        return [gateNode(0, [])],[gateNode(0, [])]
    conflictTime = [[atimList[flight] for flight in gate] + [dtimList[flight] for flight in gate] for gate in result]
    dontConflictTimeList = []
    conflictTimeList=[]
    for index1, value1 in enumerate(conflictTime):
        thisConflicts = []
        thisConflicts1=[]
        for index2, value2 in enumerate(conflictTime):
            if getConflictFlight(value1, value2) and index1!=index2:
                thisConflicts1.append(index2)
            else:
                thisConflicts.append(index2)
        newGate = gateNode(index1, thisConflicts)
        newGate1=gateNode(index1,thisConflicts1)
        conflictTimeList.append(newGate1)
        dontConflictTimeList.append(newGate)
    return dontConflictTimeList,conflictTimeList




def getHamiltonRouts(conflictTimeList):
    if len(conflictTimeList)==0 or len(conflictTimeList)==1:
        return [conflictTimeList[0].value],[conflictTimeList[0].value]
    degree = [len(node.noConflicts) for node in conflictTimeList]
    hamiltonRouts = []
    notBeChoosed=[]
    while len(hamiltonRouts) != len(degree):
        if len(hamiltonRouts) == 0:  # 初始化时得操作
            minDegreeIndex = degree.index(min(degree))
            hamiltonRouts.append(minDegreeIndex)
        else:
            lastNode = hamiltonRouts[-1]
            canBeChoosed = conflictTimeList[lastNode].noConflicts
            canBeChoosed = list(set(canBeChoosed).difference(hamiltonRouts))
            ##路径生长到不能再生长了
            if len(canBeChoosed) == 0:
                notBeChoosed = list(set(range(len(conflictTimeList))).difference(hamiltonRouts))
                s = 0
                while True:
                    if len(notBeChoosed)==0 or s>3:
                        break
                    for index, thisOne in enumerate(notBeChoosed):
                        for i in range(len(hamiltonRouts)-1):
                            if (thisOne in conflictTimeList[hamiltonRouts[i]].noConflicts and thisOne in conflictTimeList[
                                hamiltonRouts[i+1]].noConflicts and thisOne not in hamiltonRouts ) or \
                                    (i == 0 and thisOne in conflictTimeList[hamiltonRouts[i+1]].noConflicts not in hamiltonRouts ):
                                hamiltonRouts = hamiltonRouts[:i] + [thisOne] + hamiltonRouts[i:]
                    notBeChoosed = list(set(range(len(conflictTimeList))).difference(hamiltonRouts))
                    s += 1
                break
            else:
                degreeOfCanBeChoosed = [degree[item] for item in canBeChoosed]
                indexCanBeChoosed = degreeOfCanBeChoosed.index(min(degreeOfCanBeChoosed))
                hamiltonRouts.append(canBeChoosed[indexCanBeChoosed])
    return hamiltonRouts ,notBeChoosed
    # 贪心法得哈密尔顿路径

def anlysisForResult(result,typeOfResult,nationOfResult):
    # typeOfResult = [typeOfParas[item] for item in indexOfResult]
    # nationOfResult = [nationOfParas[item] for item in indexOfResult]
    interF = []
    interE = []
    interD = []
    interC = []
    nationalF = []
    nationalE = []
    nationalD = []
    nationalC = []
    for i in range(len(typeOfResult)):
        if nationOfResult[i] == 1:
            if typeOfResult[i] == 3:
                interF.append(result[i])
            elif typeOfResult[i] == 2:
                interE.append(result[i])
            elif typeOfResult[i] == 1:
                interD.append(result[i])
            else:
                interC.append(result[i])

        else:
            if typeOfResult[i] == 3:
                nationalF.append(result[i])
            elif typeOfResult[i] == 2:
                nationalE.append(result[i])
            elif typeOfResult[i] == 1:
                nationalD.append(result[i])
            else:
                nationalC.append(result[i])
    return interF,interE,interD,interC,nationalF,nationalE,nationalD,nationalC

def getParasAndBoundForSecondPro(result,nationOfResult,typeOfResult,conflictTimeList):
    parasForSecondPro = [[0 for i in range(len(result))] for j in range(len(result))]
    typeDictInter = ["C", "D", "E", "F"]
    dataBase=myDataBase()
    nationalGateInf, internationalGateInf = dataBase.gateInf()
    for i in range(len(result)):
        if nationOfResult[i] == 1:  # 国际的航班
            canBeUsedType = typeDictInter[typeOfResult[i]:]
            canBeUsedGate = internationalGateInf.loc[internationalGateInf["mdl"].isin(canBeUsedType)][
                "gateno"].to_list()
        else:
            canBeUsedType = typeDictInter[typeOfResult[i]:]
            canBeUsedGate = internationalGateInf.loc[internationalGateInf["mdl"].isin(canBeUsedType)][
                                "gateno"].to_list() + nationalGateInf.loc[nationalGateInf["mdl"].isin(canBeUsedType)][
                                "gateno"].to_list()
        # thisPara=["y%s,%s"%(i,item) for item in canBeUsedGate]
        for item in [int(gate) - 101 for gate in canBeUsedGate]:
            parasForSecondPro[i][item] = 1
    ##考虑相邻机位之间的约束关系
    # 对于边界特殊处理
    allBounds = []
    for node in conflictTimeList:
        i = node.value
        conflictWithThis = node.noConflicts
        for j in range(len(result) - 1):
            if parasForSecondPro[i][j] != 1:
                pass
            else:
                if j == 0:
                    thisBound = [[thisConf, j + 1] for thisConf in conflictWithThis if
                                 (parasForSecondPro[thisConf][j + 1] == 1 and thisConf >= i)]
                elif j == (len(result) - 1):
                    thisBound = [[thisConf, j - 1] for thisConf in conflictWithThis if
                                 (parasForSecondPro[thisConf][j - 1] == 1 and thisConf >= i)]
                else:
                    thisBound = [[thisConf, j - 1] for thisConf in conflictWithThis if
                                 (parasForSecondPro[thisConf][j - 1] == 1 and thisConf >= i)] + [[thisConf, j + 1] for   thisConf in conflictWithThis if (parasForSecondPro[thisConf][j + 1] == 1 and thisConf >= i)]
                thisBound = [[i, j]] + thisBound
                allBounds.append(thisBound)
    return parasForSecondPro,allBounds
def getPlanToGate(resultInf,internationalGateInf,nationalGateInf,atimList, dtimList):
    resultDict = {0: [1, 3], 1: [1, 2], 2: [1, 1], 3: [1, 0], 4: [0, 3], 5: [0, 2], 6: [0, 1], 7: [0, 0]}
    typeDict = ["C", "D", "E", "F"]
    ##记录各个型号的位置已经用了多少
    beUsedNumber = [[0, 0, 0, 0], [0, 0, 0, 0]]
    ##记录哪个位置已经被用了
    gatePlanDict = {}
    for index, thisResult in enumerate(resultInf):
        typeOfThisSet = resultDict[index]
        if typeOfThisSet[0] == 1:
            allCanBeUsedGate = \
            internationalGateInf.loc[internationalGateInf["mdl"].isin(typeDict[typeOfThisSet[1]:])].sort_values(
                by="mdl")[
                "gateno"].to_list()
            alreadyBeUsed = sum(beUsedNumber[1][typeOfThisSet[1]:])
        else:
            allCanBeUsedGate = \
            internationalGateInf.loc[internationalGateInf["mdl"].isin(typeDict[typeOfThisSet[1]:])].sort_values(
                by="mdl")[
                "gateno"].to_list() + \
            nationalGateInf.loc[nationalGateInf["mdl"].isin(typeDict[typeOfThisSet[1]:])].sort_values(by="mdl")[
                "gateno"].to_list()
            alreadyBeUsed = sum(beUsedNumber[1][typeOfThisSet[1]:]) + sum(beUsedNumber[0][typeOfThisSet[1]:])
        beUsedNumber[typeOfThisSet[0]][typeOfThisSet[1]] = len(thisResult)
        if len(thisResult) == 0:
            hamiltonRouts = []
            notBeChoosed = []
            thisOrder = []
        elif len(thisResult) == 1:
            hamiltonRouts = [0]
            notBeChoosed = []
            thisOrder = thisResult
        else:
            for i in range(len(set(allCanBeUsedGate).difference(gatePlanDict.keys())) - len(thisResult)):
                thisResult.append([])
            dontConflict, thisConflictTimeList = conflictForResult(atimList, dtimList, thisResult)
            hamiltonRouts, notBeChoosed = getHamiltonRouts(dontConflict)
            thisOrder = [thisResult[i] for i in hamiltonRouts]
        allCanBeUsedGate = [item for item in allCanBeUsedGate if item not in gatePlanDict.keys()]
        # allCanBeUsedGate=sorted(allCanBeUsedGate)
        for index1, order in enumerate(thisOrder):
            if order != []:
                gatePlanDict[allCanBeUsedGate[index1]] = order
            else:
                pass

    if len(gatePlanDict.keys())<(len(internationalGateInf)+len(nationalGateInf)):
        for thisKey in set([str(i) for i in internationalGateInf["gateno"].to_list()]+[str(j) for j in nationalGateInf["gateno"].to_list()]).difference(gatePlanDict.keys()):
            gatePlanDict[thisKey]=[]
    return gatePlanDict
def gateToPlanMethodsTwo(allGate,result,resultInf,atimList,dtimList,nationOfResult,typeOfResult):
    nationalType = [22, 28, 4, 1]
    internationalType = [3, 7, 2, 1]
    # gateNumber存储国内国际停机位的类型分别表示c,d,e,f
    gateSum = [nationalType, internationalType]
    beUsedGateSum = [[0, 0, 0, 0], [0, 0, 0, 0]]
    needGateSum = [[len(resultInf[7]), len(resultInf[6]), len(resultInf[5]), len(resultInf[4])],
                   [len(resultInf[3]), len(resultInf[2]), len(resultInf[1]), len(resultInf[0])]]
    # minGateNumber, maxGateNumber = allGate["gateno"].min(), allGate["gateno"].max()
    dontConflictList, conflictList = conflictForResult(atimList, dtimList, result)
    beUsedResult = []
    resultDict = {}
    tempDict = {"C": 0, "D": 1, "E": 2, "F": 3}
    for gate in range(101, 169):
        thisTypeOfGate = allGate.loc[allGate["gateno"] == str(gate)]["mdl"].iloc()[0]
        thisNationOfGate = allGate.loc[allGate["gateno"] == str(gate)]["nation"].iloc()[0]
        allCanBeChoosed = []

        if thisNationOfGate == "国际":
            # shouldEleaved = sum(needGateSum[1][:tempDict[thisTypeOfGate]+1]) - sum(
            #     [gateSum[1][i] - beUsedGateSum[1][i] for i in range(tempDict[thisTypeOfGate]+1)])

            # 说明需要从国际的分配方案里面选取
            if sum(needGateSum[1][:tempDict[thisTypeOfGate] + 1]) >= sum(gateSum[1][:tempDict[thisTypeOfGate] + 1]):
                for i in range(tempDict[thisTypeOfGate], -1, -1):
                    allCanBeChoosed.append([index for index, thisValue in enumerate(nationOfResult) if (
                            thisValue == 1 and typeOfResult[index] == i and index not in beUsedResult)])

            else:  # 说明可以从国内国外选取，优先选取国际的
                for i in range(tempDict[thisTypeOfGate], -1, -1):
                    allCanBeChoosed.append([index for index, thisValue in enumerate(nationOfResult) if
                                            (thisValue == 1 and typeOfResult[
                                                index] == i and index not in beUsedResult)])
                    allCanBeChoosed.append([index for index, thisValue in enumerate(nationOfResult) if
                                            (thisValue == 0 and typeOfResult[
                                                index] == i and index not in beUsedResult)])
        else:
            for i in range(tempDict[thisTypeOfGate], -1, -1):
                allCanBeChoosed.append([index for index, thisValue in enumerate(nationOfResult) if
                                        (thisValue == 0 and typeOfResult[index] == i and index not in beUsedResult)])

        ##从可用结果中选出与上一个机位能够相连的机位
        canBeChoose = []

        if len(resultDict.keys()) == 0:
            for item in allCanBeChoosed:
                if len(item) != 0:
                    canBeChoose = item
        else:
            previousResult = resultDict[str(int(gate) - 1)]
            for thisOne in allCanBeChoosed:  # 优先分配与改机型最对应得那个方案
                canBeChoose = [item for item in thisOne if item in dontConflictList[previousResult].noConflicts]
                if len(canBeChoose) != 0:
                    break
                elif len(canBeChoose) == 0 and len(thisOne) != 0:
                    canBeChoose = thisOne
                    break
                else:
                    pass

        dCanBeChoose = [len(set(dontConflictList[item].noConflicts).difference(beUsedResult)) for item in
                        canBeChoose]
        beChooseIndex = dCanBeChoose.index(min(dCanBeChoose))
        resultDict[str(gate)] = canBeChoose[beChooseIndex]
        thisResult = canBeChoose[beChooseIndex]
        beUsedResult.append(thisResult)
        gateSum[nationOfResult[thisResult]][typeOfResult[thisResult]] -= 1
        needGateSum[nationOfResult[thisResult]][typeOfResult[thisResult]] += 1
        if len(beUsedResult) == len(result) and max(resultDict.keys()) != "168":
            # for i in range(int(max(resultDict.keys()))-1,169):
            #     resultDict[str(i)]=[]
            for key in resultDict.keys():
                resultDict[key] = result[resultDict[key]]
            return resultDict

    return resultDict