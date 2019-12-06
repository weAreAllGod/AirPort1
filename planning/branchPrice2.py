import numpy as np
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
register_matplotlib_converters()
from tools.funcForColumn import  treeNote, searcher2,gateSearcher,gateNode,getConflictFlight
from tools.cplexFunc import cplexSoverMain,cplexSoverDual,cplexSoverSub
from tools.dataBase import myDataBase
import pandas as pd
import ast
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
mydata=dataBase.getDataOne()
print("读取完毕...")
possibles=dataBase.getPossibleOne()
print("数据准备完毕...",datetime.datetime.now()-startTime)
bridgeNumber=65
atimList=mydata["atime"].to_list()
dtimList=mydata["dtime"].to_list()

conflictSet=dict()
for i in range(len(atimList)):
    thisDtime=dtimList[i]
    thisList=[]
    for j in range(i+1,len(atimList)):
        if atimList[j]-thisDtime<pd.Timedelta("0 days 00:20:00"):
            thisList.append(j)
    conflictSet[i]=thisList


# 如果用列生成算法求，没有必要再求解开始的时候将所有的情况都列举出来，可以大大的减少
initLen=2000
c=[len(i) for  i in possibles[:initLen]]
print("子问题的冲突矩阵准备完毕....")


reMatrix=np.zeros((len(atimList)+1,len(c)))
# 近机位约束
reMatrix[0,:]=1
for i in range(len(atimList)):
    for j, possible in enumerate(possibles[:initLen]):
        if i in possible:
            reMatrix[i+1,j]=1
print("矩阵数据准备完毕",datetime.datetime.now()-startTime)

print("开始求解：",datetime.datetime.now())
b=[65]+[1 for i in range(len(atimList))]
beChoosed = [i for i in range(800)]
# 首先从前1000个变量中选取一个非零的列构成限制主问题
tempC=[c[i] for i in beChoosed]
tempReMatrix=reMatrix[:,beChoosed]
my_prob=cplexSoverMain(tempC,tempReMatrix,b,"C")
# my_prob=cplexSoverMain(c,reMatrix,b,"C")
x = my_prob.solution.get_values()
# print(my_prob.solution.get_objective_value())
beChoosed=[index for index,value in enumerate(x) if value!=0]
notBeChoosed=[i for i in range(800,reMatrix.shape[1])]
tempC=[c[i] for i in beChoosed]
tempReMatrix=reMatrix[:,beChoosed]
print(beChoosed)
#这里是列生成的过程
# 子问题的约束矩阵
sub_matrix = np.zeros((reMatrix.shape[0] - 1, reMatrix.shape[0] - 1))
for i in range(sub_matrix.shape[0]):
    for j in conflictSet[i]:
        sub_matrix[i, j] = 1


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
    sub_c=[1-i for i in x1[1:]]

    sub_b=[1 for i in range(sub_matrix.shape[0])]
    my_probs=cplexSoverSub(sub_c,sub_matrix,None,"I")
    sub_value=my_probs.solution.get_values()
    sub_object_value=my_probs.solution.get_objective_value()
    sigma=sub_object_value+(1-x[0])
    add_column=[1]+sub_value
    if sigma<=0 or jdugeConflict(add_column,tempReMatrix):
        print("已经得到最优解")
        my_prob_f=cplexSoverMain(tempC,tempReMatrix,b,"C")
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

