import matplotlib.pyplot as plt
import pandas as pd
from tools import dataBase
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
def showArraftFlight(mydata, atimList, dtimList,xlabel=None,ylabel=None,title=None):
    for i in range(len(atimList)):
        allSeconds = int((dtimList[i] - atimList[i]).total_seconds())
        if allSeconds > 0:
            plt.plot(pd.date_range(start=atimList[i], end=dtimList[i], periods=allSeconds),
                     [i for j in range(allSeconds)], linewidth=2)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            # plt.text(atimList[i], i, mydata["aflightno"].iloc[i], fontsize=4)
if __name__ == '__main__':
    #论文中显示到达分布情况的图
    db=dataBase.myDataBase()
    initialData,mydata=db.getDataThree()
    mydata=mydata.iloc[:120,:]
    atime=mydata["atime"].to_list()
    dtime=mydata["dtime"].to_list()
    showArraftFlight(mydata,atime,dtime,xlabel="time",ylabel="aircraft",title="Flight distribution")
