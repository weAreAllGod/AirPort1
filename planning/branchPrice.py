import numpy as np
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
register_matplotlib_converters()
from tools.funcForColumn import  treeNote, searcher2,gateSearcher,gateNode,getConflictFlight
from tools.cplexFunc import cplexSoverMain,cplexSoverDual
from tools.dataBase import myDataBase
import pandas as pd
import ast
import datetime
# 基础数据
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
c=[len(i) for  i in possibles]

reMatrix=np.zeros((len(atimList)+1,len(possibles)))
# 近机位约束
reMatrix[0,:]=1
for i in range(len(atimList)):
    for j, possible in enumerate(possibles):
        if i in possible:
            reMatrix[i+1,j]=1
print("矩阵数据准备完毕",datetime.datetime.now()-startTime)
b=[65]+[1 for i in range(len(atimList))]

beChoosed = [i for i in range(3000)]
# 首先从前1000个变量中选取一个非零的列构成限制主问题
tempC=[c[i] for i in beChoosed]
tempReMatrix=reMatrix[:,beChoosed]
my_prob=cplexSoverMain(tempC,tempReMatrix,b,"C")
# my_prob=cplexSoverMain(c,reMatrix,b,"C")
x = my_prob.solution.get_values()
# print(my_prob.solution.get_objective_value())
beChoosed=[index for index,value in enumerate(x) if value!=0]
notBeChoosed=[i for i in range(1000,reMatrix.shape[1])]
print(beChoosed)
#这里是列生成的过程
while True:
    tempC=[c[i] for i in beChoosed]
    tempReMatrix=reMatrix[:,beChoosed]
    # result=[possibles[index] for index,value in enumerate(x) if value==1]
    # print("靠桥率：",sum([len(item) for item in result])/len(atimList))
    # print(x)
    # my_prob.write("../state/data/problem.lp")
    # my_prob.solution.write("../state/data/result.lp")
    print("------------------------>以下为对偶问题<----------------------------")
    # 对偶问题
    d_c=b
    d_reMatrix=tempReMatrix.T
    d_b=tempC
    my_prob=cplexSoverDual(d_c,d_reMatrix,d_b,"C")
    x1 = my_prob.solution.get_values()
    maxSigma=-np.inf
    maxSigmaI=-np.inf
    test=[]
    for i in notBeChoosed:
        thisAj=reMatrix[:,i]
        # 这一列首先要满足所有的条件，并且检验数大于0
        sigma=c[i]-np.dot(np.array(x1),thisAj)
        test.append(sigma)
        if sigma>0 and sigma>maxSigma :
            maxSigma=sigma
            maxSigmaI=i
    # 判断检验数
    if maxSigma<=0:

        # 全局最优解是103
        # result=[possibles[index] for index,value in enumerate(x) if value==1]
        my_prob = cplexSoverMain(tempC, tempReMatrix, b, "C")
        x = my_prob.solution.get_values()
        objectValue = my_prob.solution.get_objective_value()
        if(objectValue==103):
            print("躺尸一天！！！！！！！！！")
        else:
            print("本次最优解：",objectValue)
        break
    else:
        beChoosed.append(maxSigmaI)
        notBeChoosed.remove(maxSigmaI)
# 接下来是分支定价的过程
import math
while True:
    for i in x:
        if i!=0 or math.floor(i)==math.ceil(i):
            pass
        else:
            print(i)
            print("分支定界")
    print("已经是最优解")
    break

