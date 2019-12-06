
from  tools.dataBase import myDataBase
def analysisOfPlans(result,data,dataNearByHum,resultInf,atimList):

    print("---------------------------第一阶段求解结果报告-----------------------------")
    print("总飞机个数：", len(data))
    print("过夜航班个数：",len(data)-len(atimList))
    print("算法分配靠桥飞机数：",sum([len(item) for item in result]) )
    print("算法分配靠桥比率：", sum([len(item) for item in result]) / len(data))
    if len(dataNearByHum)!=0:
        print("人工分配靠桥飞机数：",dataNearByHum.shape[0])
        print("人工分配靠桥比率：", dataNearByHum.shape[0]/len(atimList))
    else:
        print("没有人工分配的数据与之对比。")
    print("---------------------------各个分配方案的类型报告-----------------------------")


    print("国际航班F型方案，共%s"%(len(resultInf[0])))
    print(resultInf[0])

    print("国际航班E型方案，共%s" % (len(resultInf[1])))
    print(resultInf[1])

    print("国际航班D型方案，共%s" % (len(resultInf[2])))
    print(resultInf[2])

    print("国际航班C型方案，共%s" % (len(resultInf[3])))
    print(resultInf[3])

    print("国内航班F型方案，共%s" % (len(resultInf[4])))
    print(resultInf[4])

    print("国内航班E型方案，共%s" % (len(resultInf[5])))
    print(resultInf[5])

    print("国内航班D型方案，共%s" % (len(resultInf[6])))
    print(resultInf[6])

    print("国内航班C型方案，共%s" % (len(resultInf[7])))
    print(resultInf[7])
    #
    #
    # print("---------------------------第二阶段求解结果报告-----------------------------")
    # if len(hamiltonRouts) == len(conflictTimeList):
    #     print("第二阶段得到一条通路，全局最优解得到,最终排序结果：")
    #     print(hamiltonRouts)
    # else:
    #     print("第二阶段没有得到一条通路,有%s" % (len(notBeChoosed)))
    #     print("这几个方案得下标是:", notBeChoosed)
    #     print("如果放松机位之间得时间约束可以得方案是...")
    #     print("他们之间得间隔时间是...")
def gateToPlan(gatePlanDict,atimList,dtimList,numberOfPlan,nationOfPlan,typeOfplan,allGate):
    minGateNumber = min(gatePlanDict.keys())

    print("-------------------详细的分配结果如下-----------------------")
    for key in sorted(gatePlanDict.keys()):
        conflictInf = []
        if key != minGateNumber:
            previousPlan = gatePlanDict[str(int(key) - 1)]
            thisPlan = gatePlanDict[key]
            for plan in thisPlan:
                for pPlan in previousPlan:
                    allSeconds = (atimList[plan] - atimList[pPlan]).seconds if (atimList[plan] - atimList[
                        pPlan]).days > 0 else (atimList[pPlan] - atimList[plan]).seconds
                    allSeconds1 = (atimList[plan] - dtimList[pPlan]).seconds if (atimList[plan] - dtimList[
                        pPlan]).days > 0 else (dtimList[pPlan] - atimList[plan]).seconds
                    allSeconds2 = (dtimList[plan] - atimList[pPlan]).seconds if (dtimList[plan] - atimList[
                        pPlan]).days > 0 else (atimList[pPlan] - dtimList[plan]).seconds
                    allSeconds3 = (dtimList[plan] - dtimList[pPlan]).seconds if (dtimList[plan] - dtimList[
                        pPlan]).days > 0 else (dtimList[pPlan] - dtimList[plan]).seconds
                    if allSeconds < 60 * 10:
                        conflictInf.append("\033[0;31m%s的进机位时间与%s的进机位时间，时间间隔为\033[5;33m%s分钟\033[0m " % (
                        numberOfPlan[plan], numberOfPlan[pPlan], allSeconds / 60))
                    elif allSeconds1 < 60 * 10:
                        conflictInf.append("\033[0;31m%s的进机位时间与%s的出机位的时间,时间间隔为\033[5;33m%s分钟\033[0m " % (
                        numberOfPlan[plan], numberOfPlan[pPlan], allSeconds1 / 60))
                    elif allSeconds2 < 60 * 10:
                        conflictInf.append("\033[0;31m%s的出机位时间与%s的进机位的时间,时间间隔为\033[5;33m%s分钟\033[0m " % (
                        numberOfPlan[plan], numberOfPlan[pPlan], allSeconds2 / 60))
                    elif allSeconds3 < 60 * 10:
                        conflictInf.append("\033[0;31m%s的出机位时间与%s的出机位的时间,时间间隔为\033[5;33m%s分钟\033[0m " % (
                        numberOfPlan[plan], numberOfPlan[pPlan], allSeconds3 / 60))
            if len(conflictInf) == 0:
                # \033[0;32;40m 显示方式；前景色，背景色，m
                conflictInf.append("\033[0;32m%s进机位与%s进机位不存在时间冲突\033[0m" % (key, str(int(key) - 1)))
        for inf in conflictInf:
            print(inf, end="")
        print("\n", end="")
        print("停机位%s(%s,%s)" % (
        key, allGate[allGate["gateno"] == key]["mdl"].iloc()[0], allGate[allGate["gateno"] == key]["nation"].iloc()[0]),
              [(numberOfPlan[i] + ("|国内" if nationOfPlan[i] == 0 else "国际") + typeOfplan[i] + "型",
                str(atimList[i])[-8:] + "-" + str(dtimList[i])[-8:]) for i in gatePlanDict[key]])

        # finallBeChoosed = []
        # for plan in result:
        #     finallBeChoosed += plan
        # finallNotBeChoosed = set(range(len(atimList))).difference(finallBeChoosed)
        #
        # remoteParkingPosition = mydata.iloc[list(finallNotBeChoosed)]
