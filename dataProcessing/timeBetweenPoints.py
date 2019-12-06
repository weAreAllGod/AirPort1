import pandas as pd
import  ast
import math
import numpy as np
mydata=pd.read_csv("../state/data/time_spend.csv")
time=[]
for item in mydata.iterrows():
    if item[1]["start_point"]==item[1]["end_point"]:
        time.append(0)
    else:
        timeList=ast.literal_eval(item[1]["time"])
        std=np.std(timeList,ddof=1)
        timeList.sort()
        thisAveTime=np.average(timeList[:int(len(timeList)*0.3+1)])
        time.append(thisAveTime)
mydata.loc[:,"timeBeChoosed"]=time
mydata.to_csv("../state/data/timeBetweenP2P.csv")