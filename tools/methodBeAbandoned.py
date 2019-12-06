from tools.funcForColumn import  gateSearcher

def hamildunRouts(conflictTimeList):
    gateS = gateSearcher()
    bridgeNumber=len(conflictTimeList)
    print("排序结果")
    finallR = []
    for i in range(bridgeNumber):
        gateS.finallyResult = []
        for node in conflictTimeList:
            node.myPointer = 0
        gateS.searchGateNode(conflictTimeList, conflictTimeList[i], [])
        print("%s最终分配的长度" % i)
        print(len(gateS.finallyResult))
        if len(gateS.finallyResult) == bridgeNumber:
            finallR = gateS.finallyResult
            print("得到最终结果：")
            print(gateS.finallyResult)
            break
        elif (len(gateS.finallyResult) > len(finallR)):
            finallR = gateS.finallyResult
            ##未被分配

        # 这里进行后续的优化操作
        notBeChoosed = set(range(len(conflictTimeList))).difference(finallR)
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
    return finallR