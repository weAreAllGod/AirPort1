from dataProcessing import service
import matplotlib.pyplot as plt
import pandas as pd
def filterComeAndGo(line):
    if line["dep_cty_chn_nm"]=="昆明":
        return line["dpt_dt"]
    else:
        return  line["arrv_dt"]

def getSeconds(line):
    periods=line["arrv_dt"]-line["schd_arrv_dt"]
    day=periods.days
    if day>=0:
        allSeconds=periods.seconds/60
    else:
        allSeconds = -(line["schd_arrv_dt"]-line["arrv_dt"]).seconds/60
    return allSeconds

def changDataForSpss(data):
    data["arrv_dt"] = data["arrv_dt"].apply(lambda x: x.strftime('%d-%m-%Y %H:%M:%S'))
    # noNoneForArrvAndSchd["dpt_dt"] = noNoneForArrvAndSchd["dpt_dt"].apply(lambda x: x.strftime('%d-%m-%Y %H:%M:%S'))
    # noNoneForArrvAndSchd["estmt_arrv_dt"] = noNoneForArrvAndSchd["estmt_arrv_dt"].apply(lambda x: x.strftime('%d-%m-%Y %H:%M:%S'))
    # noNoneForArrvAndSchd["estmt_dpt_dt"] = noNoneForArrvAndSchd["estmt_dpt_dt"].apply(
    #     lambda x: x.strftime('%d-%m-%Y %H:%M:%S'))
    data["schd_arrv_dt"] = noNoneForArrvAndSchd["schd_arrv_dt"].apply(
        lambda x: x.strftime('%d-%m-%Y %H:%M:%S'))
    # noNoneForArrvAndSchd["schd_dpt_dt"] = noNoneForArrvAndSchd["schd_dpt_dt"].apply(
    #     lambda x: x.strftime('%d-%m-%Y %H:%M:%S'))
    data.to_csv("../state/data/anlysisForDelay/dataForSPSS/到达航班延误时间.csv",encoding="gbk")
def sliceAday(timestamp):
    startOfThisDay=pd.Timestamp("%s-%s-%s 00:00:00"%(timestamp.year,timestamp.month,timestamp.day))
    allSeconds=(timestamp-startOfThisDay).seconds
    peiod=int(allSeconds/(60*10))
    return ("%s-%s-%s")%(timestamp.month,timestamp.day,peiod)


class figureShow():
    def plotScatter(self,list2,title):
        plt.figure()
        plt.scatter(range(len(list2)),list2)
        plt.title(title)

import copy


if __name__ == '__main__':
    arriveData=service.getData("arraveData",startTime="2018-01-01 00:00:00",endTime="2018-02-01 00:00:00")
    # myColumns=arriveData.columns.to_list()
    # myColumns.append("timeFromHere")
    # arriveData.columns=myColumns
    # arriveData["timeFromHere"] =pd.Series([None for i in range(arriveData.shape[0])])
    ##只考虑到达飞机
    arriveHere=arriveData.loc[arriveData["arrv_cty_chn_nm"]=="昆明"]

    outOfHere=arriveData.loc[(arriveData["dep_cty_chn_nm"]=="昆明")&(arriveData["dpt_dt"].notnull())]

    ##排序之后重新索引
    arriveTime=arriveHere.arrv_dt
    outTime=outOfHere.sort_values(by="dpt_dt").dpt_dt.reset_index(drop=True)
    # outTime=outTime.reindex(pd.Series([i for i in range(len(outTime))]))
    arriveData["timeFromHere"]=arriveData.apply(filterComeAndGo,axis = 1)
    comeAndGo=arriveData.loc[arriveData["timeFromHere"].notnull()]["timeFromHere"].reset_index(drop=True)
    # arriveTime.plot()
    # 分析到达延误情况
    noNoneForArrvAndSchd=copy.deepcopy(arriveData.loc[(arriveData["arrv_cty_chn_nm"]=="昆明")&(arriveData["arrv_dt"].notnull())&(arriveData["schd_arrv_dt"].notnull())])
    noNoneForArrvAndSchd["delayTime"] = noNoneForArrvAndSchd.apply(getSeconds, axis=1)
    noNoneForArrvAndSchd["schd_ah"]=noNoneForArrvAndSchd["schd_arrv_dt"].apply(lambda  x:pd.Timestamp(("%s-%s-%s %s:00:00")%(x.year,x.month,x.day,x.hour)))
    noNoneForArrvAndSchd["schd_period"]=noNoneForArrvAndSchd["schd_arrv_dt"].apply(sliceAday)
    # noNoneForArrvAndSchd["schd_am"] = noNoneForArrvAndSchd["schd_arrv_dt"].apply(lambda x: x.minute)
    noNoneForArrvAndSchd.to_csv("../state/data/anlysisForDelay/到达航班延误时间.csv",encoding="gbk")
    changDataForSpss(noNoneForArrvAndSchd)
    # noNoneForArrvAndSchd["delayTime"].plot()
    noNoneForArrvAndSchd=noNoneForArrvAndSchd.sort_values(by="schd_arrv_dt")
    showFigure=figureShow()
    # showFigure.plotScatter(noNoneForArrvAndSchd["delayTime"].to_list()[:3000])
    # plt.show()
    # 统计量
    # 每个小时内比预计晚到的飞机的百分比
    numberOfEh=noNoneForArrvAndSchd.groupby("schd_ah").apply(lambda x: (len([i for i in x["delayTime"] if float(i)>0])))
    percenEveryH=noNoneForArrvAndSchd.groupby("schd_ah").apply(lambda x: (len([i for i in x["delayTime"] if float(i)>0])/len(x)))

    # 每个切分的时间段内的飞机晚到的百分比
    numberOfEp=noNoneForArrvAndSchd.groupby("schd_period").apply(lambda x: (len([i for i in x["delayTime"] if float(i)>15])))
    percenEveryPeriod=noNoneForArrvAndSchd.groupby("schd_period").apply(lambda x: (len([i for i in x["delayTime"] if float(i)>15])/len(x)))

    showFigure.plotScatter(percenEveryH.to_list(),"percenEh")
    showFigure.plotScatter(percenEveryPeriod.to_list(),"percenEp")
    showFigure.plotScatter(numberOfEh.to_list(),"numberOfEh")
    showFigure.plotScatter(numberOfEp.to_list(),"numberOfEp")
    plt.show()
