import numpy as np
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
register_matplotlib_converters()
from tools  import funcForColumn
from tools.cplexFunc import cplexSoverMain,cplexSoverDual,cplexSoverBranchPrice
from tools.dataBase import myDataBase
import pandas as pd
import ast
from planning import withNationAndInternational
import datetime
import queue
def judgeAllInteger(x):
    for i in x:
        if int(i)==i:
            pass
        else:
            return False
    return True

class branchPro:
    def __init__(self,beChoosed,b1,boundIndexList1):
        # self.c=c1
        # self.matrix=matrix1
        self.beChoosed=beChoosed
        self.b=b1
        self.boundIndexList=boundIndexList1


# 基础数据
dataBase=myDataBase()
startTime=datetime.datetime.now()
print("数据准备中...")
initalData,data=dataBase.getDataThree()
mydata=data.iloc[:80,:]
nationalType = [22, 28, 4, 1]
internationalType = [3, 7, 2, 1]
numberOfTypeForPlan = mydata["mdl"].apply(lambda x: withNationAndInternational.getTypeOfPosition(x[-1])).to_list()
nationOfPlan=mydata["nation"].to_list()


print("读取完毕...")
# possibles=dataBase.getPossibleOne()

bridgeNumber=65
atimList=mydata["atime"].to_list()
dtimList=mydata["dtime"].to_list()


listNodes=[]
lenAtimeList = len(atimList)
for i in range(lenAtimeList):
    thisDtime = dtimList[i]
    thisList = []
    for j in range(i + 1, lenAtimeList):
        if atimList[j] - thisDtime > pd.Timedelta("0 days 00:20:00"):
            thisList.append(j)
    thisNode = funcForColumn.treeNote(i, thisList)
    listNodes.append(thisNode)
possibles = funcForColumn.searcher2(listNodes)
typeOfParas = []
nationOfParas = []

for everyPara in possibles:
    typeOfParas.append(max([numberOfTypeForPlan[i] for i in everyPara]))
    nationOfParas.append(max([nationOfPlan[i] for i in everyPara]))
print("数据准备完毕...",datetime.datetime.now()-startTime)
c=[len(i) for  i in possibles]
passengers=[]
for flt in mydata.iterrows():
    passengers.append(flt[1]["apassenger"]+flt[1]["dpassenger"])
pc=[]
for fa in possibles:
    totalNumer=0
    for i in fa:
        totalNumer+=passengers[i]
    pc.append(totalNumer)
c=pc
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
b[1] = sum(internationalType[-2:])
b[2] = sum(internationalType[-3:])
b[3] = sum(internationalType)

b[4] = internationalType[3] + nationalType[3]
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
print("数据准备完毕")
"""这里进行验证
"""
###求理论最优值
# c_all=[len(i) for  i in possibles]
#
# my_sense_all=""
# for i in range(reMatrix.shape[0]):
#     my_sense_all+="L"
# bestValueInTheore=cplexSoverMain(c_all,reMatrix,b,"C",my_sense_all)
# print("本问题的理论最优值为",bestValueInTheore.solution.get_objective_value())
# print("理论最优解：")
# senseIntheory=""
# for i in range(len(b)):
#     senseIntheory+="L"
# proIntheory=cplexSoverMain(c,reMatrix,b,"I",senseIntheory,)
#
# print("理论最优值：",proIntheory.solution.get_objective_value())
# print("最优的解为：")
# solutionInTheory=proIntheory.solution.get_values()
# print(solutionInTheory)

beChoosed = list(np.random.randint(0,len(c)-1,136))
# 首先从前1000个变量中选取一个非零的列构成限制主问题
tempC=[c[i] for i in beChoosed]
tempReMatrix=reMatrix[:,beChoosed]
my_sense = ""
for i in range(tempReMatrix.shape[0]):
    my_sense += 'L'
my_prob=cplexSoverMain(tempC,tempReMatrix,b,"C",my_sense)
# my_prob=cplexSoverMain(c,reMatrix,b,"C")
x = my_prob.solution.get_values()
# print(my_prob.solution.get_objective_value())
# 初始的问题根节点
# beChoosed=[index for index,value in enumerate(x) if value!=0]
# notBeChoosed=[i for i in range(20000,reMatrix.shape[1])]

print(beChoosed)
#这里是列生成的过程
print("列生成开始：")
timeBeginDW=datetime.datetime.now()


bestIntegerObjValue=-np.inf
bestIntegerValues=[]

tempC=[c[i] for i in beChoosed]
tempReMatrix=reMatrix[:,beChoosed]

problemQue=queue.Queue()
initalPro=branchPro(beChoosed,b,[])
problemQue.put(initalPro)
sizeOfPro=[]
while problemQue.empty()!=True:
    if problemQue.empty():
        print("节点列表为空，跳出来了")
        break
    print("当前最优解",bestIntegerObjValue)
    print("当前的队列长度",problemQue.qsize())

    thisPro=problemQue.get()
    cForThisPro=[c[i] for i in thisPro.beChoosed]
    matrixForThisPro=reMatrix[:,thisPro.beChoosed]
    bForThisPro=thisPro.b
    bounbForTisPro=thisPro.boundIndexList
    sizeOfPro.append(len(cForThisPro))
    print(sizeOfPro)
    my_sense1=""
    for i in range(len(b)):
        my_sense1+="L"


    my_prob = cplexSoverBranchPrice(cForThisPro,matrixForThisPro ,bForThisPro, None,my_sense1,bounbForTisPro)
    try:
        x = my_prob.solution.get_values()
    except:
        ##一旦无解，放弃这个分支
        print("无解的情况")
        continue
    thisObjValue = my_prob.solution.get_objective_value()
    print("当前松弛最优解",thisObjValue)
    if judgeAllInteger(x) and thisObjValue>bestIntegerObjValue:
        bestIntegerObjValue=thisObjValue
        bestIntegerValues=x

    #如果这个分支的松弛最优解不如目前最优解，那么放弃这个分支
    if round(thisObjValue,4)<round(bestIntegerObjValue,4):#对于精度问题问题产生的错误要考虑，
        print("不如最优解砍掉")
        continue

    print("这是本次的解X",x)
    x1 = my_prob.solution.get_dual_values()
    # notBeChoosed = sorted(list(set(range(len(c))).difference(thisPro.beChoosed)))
    thisReMatrix = reMatrix.T

    sigmas = np.array(c) - np.sum(thisReMatrix * np.array(x1), axis=1)
    maxSigma = sigmas.max()
    maxSigmaI = sigmas.argmax()
    print("当前的sigma",maxSigma)
    if maxSigma <= 0.01 or (maxSigmaI in thisPro.beChoosed):
        # 这是松弛问题最优解
        isAllInteger = True
        for index, thisSol in enumerate(x):
            if int(thisSol) == thisSol:
                # 说明是整数
                pass
            else:
                onePro = branchPro(thisPro.beChoosed, bForThisPro, bounbForTisPro + [[index, 0]])
                twoPro = branchPro(thisPro.beChoosed, thisPro.b, bounbForTisPro + [[index, 1]])
                problemQue.put(onePro)
                problemQue.put(twoPro)
                isAllInteger = False
                break
        if isAllInteger:
            print("找到最优解了，别循环了")
            endTime=datetime.datetime.now()
            print("总共用时：",endTime-timeBeginDW)
            break
    else:
        newPro = branchPro(thisPro.beChoosed + [maxSigmaI], b, thisPro.boundIndexList)
        problemQue.put(newPro)
print("节点列表为空了")
endTime=datetime.datetime.now()
print("总共用时：",endTime-timeBeginDW)







    #
    #
    #
    # isAllInteger=True
    # for index,thisSol in enumerate(x):
    #     if int(thisSol)==thisSol:
    #         #说明是整数
    #         pass
    #     else:
    #         onePro = branchPro(thisPro.beChoosed, bForThisPro,bounbForTisPro + [[index, 0]])
    #         twoPro = branchPro(thisPro.beChoosed, thisPro.b, bounbForTisPro+[[index, 1]])
    #
    #
    #
    #
    #         problemQue.put(onePro)
    #         problemQue.put(twoPro)
    #         isAllInteger=False
    #         break
    # if isAllInteger:
    #     #首先记下本次的最优解
    #     print("进入最优解判断")
    #     if thisObjValue>bestIntegerObjValue:
    #         bestIntegerObjValue=thisObjValue
    #         bestIntegerValues=my_prob.solution.get_values()
    #     ##说明结果全是整数，此时计算检验数，是否还需要再次进行添加列
    #     x1=my_prob.solution.get_dual_values()
    #     notBeChoosed = sorted(list(set(range(len(c))).difference(thisPro.beChoosed)))
    #     thisReMatrix = reMatrix[:,notBeChoosed].T
    #
    #     sigmas = np.array([c[i] for i in notBeChoosed]) - np.sum(thisReMatrix * np.array(x1), axis=1)
    #     maxSigma = sigmas.max()
    #     maxSigmaI = sigmas.argmax()
    #
    #     print("本次的sigma:",maxSigma)
    #     if maxSigma <= 0.01 or len(notBeChoosed)==0:
    #         # 这就是最优解了
    #         print("这就是最优解了")
    #         break
    #     else:
    #         newPro=branchPro(thisPro.beChoosed+[notBeChoosed[maxSigmaI]],b,thisPro.boundIndexList)
    #         problemQue.put(newPro)
    # else:
    #     pass
    #
    #
    #


    # tempC=[c[i] for i in beChoosed]
    # tempReMatrix=reMatrix[:,beChoosed]
    # result=[possibles[index] for index,value in enumerate(x) if value==1]
    # print("靠桥率：",sum([len(item) for item in result])/len(atimList))
    # print(x)
    # my_prob.write("../state/data/problem.lp")
    # my_prob.solution.write("../state/data/result.lp")
#     print("------------------------>以下为对偶问题<----------------------------")
#     # 对偶问题
#     d_c=b
#     d_reMatrix=tempReMatrix.T
#     d_b=tempC
#     my_prob=cplexSoverDual(d_c,d_reMatrix,d_b,"C")
#     x1 = my_prob.solution.get_values()
#
#     thisReMatrix=reMatrix.T
#     sigmas=np.array(c)-np.sum(thisReMatrix*np.array(x1),axis=1)
#     maxSigma =sigmas.max()
#     maxSigmaI=sigmas.argmax()
#
#
#     # for i in range(reMatrix.shape[1]):
#     #     thisAj=reMatrix[:,i]
#     #     # 这一列首先要满足所有的条件，并且检验数大于0
#     #     sigma=c[i]-np.dot(np.array(x1),thisAj)
#     #     if sigma>0 and sigma>maxSigma :
#     #         maxSigma=sigma
#     #         maxSigmaI=i
#     # 判断检验数
#     print("本次的检验数：",maxSigma)
#     if maxSigma<=0.01 or (maxSigmaI in beChoosed):
#
#         result=[possibles[index] for index,value in enumerate(x) if value==1]
#         my_sense1=""
#         for i in range(tempReMatrix.shape[0]):
#             my_sense1+="L"
#         my_prob = cplexSoverMain(tempC, tempReMatrix, b, "C",my_sense1)
#         x = my_prob.solution.get_values()
#         objectValue = my_prob.solution.get_objective_value()
#         timeEndDW=datetime.datetime.now()
#         print("本次最优解：", objectValue)
#         print("列生成总共耗时：",timeEndDW-timeBeginDW)
#         # print("接下来是分支定界的过程：")
#         # problemQue=queue.Queue()
#         # initalPro=branchPro(tempC,tempReMatrix,b,[])
#         # problemQue.put(initalPro)
#         # bestIntegerValues=None
#         # bestIntegerObject=-np.inf
#         # while not problemQue.empty():
#         #     #取出一个进行求解
#         #     thisPro=problemQue.get()
#         #     print(thisPro.boundIndexList)
#         #     my_sense1=""
#         #     for i in range(thisPro.matrix.shape[0]):
#         #         my_sense1+="L"
#         #     my_prob = cplexSoverBranchPrice(thisPro.c, thisPro.matrix, thisPro.b, "C",my_sense1,thisPro.boundIndexList)
#         #     x = my_prob.solution.get_values()
#         #     #如果松弛后的最优解都没有历史最优解好，就放弃
#         #     if my_prob.solution.get_objective_value()<bestIntegerObject:
#         #         continue
#         #     gard=True
#         #     for index,value in enumerate(x):
#         #         #说明不是整数
#         #         if int(value)!=value:
#         #             #解这个问题，并求其影子价格
#         #             onePro=branchPro(thisPro.c, thisPro.matrix, thisPro.b,thisPro.boundIndexList+[[index,0]])
#         #             twoPro = branchPro(thisPro.c, thisPro.matrix, thisPro.b, thisPro.boundIndexList+[[index, 1]])
#         #             problemQue.put(onePro)
#         #             problemQue.put(twoPro)
#         #             gard=False
#         #             break
#         #         else:
#         #             pass
#         #         ##说明这个分支产生了整数最优解
#         #     if my_prob.solution.get_objective_value()>bestIntegerObject and gard:
#         #         bestIntegerObject=my_prob.solution.get_objective_value()
#         #         bestIntegerValues=x
#         #     else:
#         #         pass
#         # ##当这些都结束，输出bestIntegerObject,bestIntegerValues
#         # print(bestIntegerValues)
#     else:
#         beChoosed.append(maxSigmaI)
# # 接下来是分支定价的过程
# # import math
# # while True:
# #     for i in x:
# #         if i!=0 or math.floor(i)==math.ceil(i):
# #             pass
# #         else:
# #             print(i)
# #             print("分支定界")
# #     print("已经是最优解")
# #     break

