import numpy as np
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
register_matplotlib_converters()
from tools import funcForColumn
from tools.funcForColumn import  treeNote, searcher2,gateSearcher,gateNode,getConflictFlight
from tools.cplexFunc import cplexSoverMain,cplexSoverDual,cplexSoverSub
from tools.dataBase import myDataBase
import pandas as pd
from planning import withNationAndInternational
import datetime
# 基础数据
def jdugeConflict(add_column,tempReMatrix):
    for i in range(tempReMatrix.shape[1]):

        if (list(tempReMatrix[:, i]) == add_column):
            print(i)
            print(add_column)
            print(tempReMatrix[:, i])
            print("已经是最优解....")
            return True
    return False

dataBase=myDataBase()
startTime=datetime.datetime.now()
print("数据准备中...")
initialData,data = dataBase.getDataThree()
mydata=data.iloc[:220,:]
print("读取读取完毕...")

bridgeNumber=65
atimList=mydata["atime"].to_list()
dtimList=mydata["dtime"].to_list()
nationalType = [22, 28, 4, 1]
internationalType = [3, 7, 2, 1]
numberOfTypeForPlan = mydata["mdl"].apply(lambda x: withNationAndInternational.getTypeOfPosition(x[-1])).to_list()
nationOfPlan=mydata["nation"].to_list()

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
print("变量构建完毕...")
typeOfParas = []
nationOfParas = []
for everyPara in possibles:
    typeOfParas.append(max([numberOfTypeForPlan[i] for i in everyPara]))
    nationOfParas.append(max([nationOfPlan[i] for i in everyPara]))

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

###求理论最优值
# c_all=[len(i) for  i in possibles]
# my_sense_all=""
# for i in range(reMatrix.shape[0]):
#     my_sense_all+="L"
# bestValueInTheore=cplexSoverMain(c_all,reMatrix,b,"C",my_sense_all)
# print("本问题的理论最优值为",bestValueInTheore.solution.get_objective_value())
# 如果用列生成算法求，没有必要再求解开始的时候将所有的情况都列举出来，可以大大的减少

initLen=2000
print("列生成过程开始！选前%s个变量作为初始值"%(initLen))
c=[len(i) for  i in possibles[:initLen]]
initialBeChoosed = [i for i in range(initLen)]
# 首先从前1000个变量中选取一个非零的列构成限制主问题
tempC=[c[i] for i in initialBeChoosed]
tempReMatrix=reMatrix[:,initialBeChoosed]
my_sense = ""
for i in range(tempReMatrix.shape[0]):
    my_sense += 'L'


my_prob=cplexSoverMain(tempC,tempReMatrix,b,"C",my_sense)
# my_prob=cplexSoverMain(c,reMatrix,b,"C")
x = my_prob.solution.get_values()
# print(my_prob.solution.get_objective_value())
beChoosed=[index for index,value in enumerate(x) if value!=0]
# notBeChoosed=[i for i in range(initLen,reMatrix.shape[1])]
tempC=[c[i] for i in beChoosed]
tempReMatrix=reMatrix[:,beChoosed]
print(beChoosed)
#这里是列生成的过程
# 子问题的约束矩阵,表示每个列变量中各个元素之间的关系

conflictSet=dict()
for i in range(len(atimList)):
    thisDtime=dtimList[i]
    thisList=[]
    for j in range(i+1,len(atimList)):
        if atimList[j]-thisDtime<pd.Timedelta("0 days 00:20:00"):
            thisList.append(j)
    conflictSet[i]=thisList

sub_matrix = np.zeros((lenAtimeList, lenAtimeList))
for i in range(sub_matrix.shape[0]):
    for j in conflictSet[i]:
        sub_matrix[i, j] = 1
print("子问题冲突矩阵准备完毕")

while True:


    # result=[possibles[index] for index,value in enumerate(x) if value==1]
    # print("靠桥率：",sum([len(item) for item in result])/len(atimList))
    # print(x)
    # my_prob.write("../state/data/problem.lp")
    # my_prob.solution.write("../state/data/result.lp")
    print("------------------------>以下为对偶问题<----------------------------")
    # 对偶问题
    d_c=b
    d_reMatrix=tempReMatrix.T
    d_b = tempC
    my_prob_d=cplexSoverDual(d_c,d_reMatrix,d_b,"C")
    x1 = my_prob_d.solution.get_values()
    # maxSigma=-np.inf
    # maxSigmaI=-np.inf
    # test=[]
    # # 第一种方法
    # for i in notBeChoosed:
    #     thisAj=reMatrix[:,i]
    #     # 这一列首先要满足所有的条件，并且检验数大于0
    #     sigma=c[i]-np.dot(np.array(x1),thisAj)
    #     test.append(sigma)
    #     if sigma>0 and sigma>maxSigma :
    #         maxSigma=sigma
    #         maxSigmaI=i
    # 第二种方法
    print("开始解子问题")
    sub_c=[1-xx*bb for xx,bb in zip(x1,b)]

    sub_b=[1 for i in range(sub_matrix.shape[0])]
    my_probs=cplexSoverSub(sub_c,sub_matrix,None,"I")
    sub_value=my_probs.solution.get_values()
    sub_object_value=my_probs.solution.get_objective_value()
    sigma=sub_object_value+(1-x[0])
    add_column=[1]+sub_value
    if sigma<=0.001 or jdugeConflict(add_column,tempReMatrix):
        print("已经得到最优解")
        my_sense1=""
        for i in range(tempReMatrix.shape[0]):
            my_sense1+="L"
        my_prob_f=cplexSoverMain(tempC,tempReMatrix,b,"C",my_sense1)
        print("最优解是：",my_prob_f.solution.get_objective_value())
        print("时间",datetime.datetime.now())
        break
    else:
        tempC.append(sum(sub_value))
        tempReMatrix=np.c_[tempReMatrix,add_column]






    # # 判断检验数
    # if maxSigma<=0:
    #
    #     # 全局最优解是103
    #     # result=[possibles[index] for index,value in enumerate(x) if value==1]
    #     my_prob = cplexSoverMain(tempC, tempReMatrix, b, "C")
    #     x = my_prob.solution.get_values()
    #     objectValue = my_prob.solution.get_objective_value()
    #
    #     if(objectValue==103):
    #         print("躺尸一天！！！！！！！！！")
    #     else:
    #         print("本次最优解：",objectValue)
    #     break
    # else:
    #     beChoosed.append(maxSigmaI)
    #     notBeChoosed.remove(maxSigmaI)
# 接下来是分支定价的过程
# import math
# while True:
#     for i in x:
#         if i!=0 or math.floor(i)==math.ceil(i):
#             pass
#         else:
#             print(i)
#             print("分支定界")
#     print("已经是最优解")
#     break

