import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import numpy as np
from dataProcessing import service

my_data=service.getData("departure")
# 数据类型dtype: timedelta64[ns]
timeInterval=my_data['fatd'].diff()
timeInterval.rename(columns = 'interval')
# 转化为dtype: timedelta64[s]
timeInterval=timeInterval.astype("timedelta64[s]")
col_name=my_data.columns.tolist()
col_name.append('timeinterval')
my_data.reindex(columns=col_name)

# my_data.join(timeInterval)
pd.Series([0]).append(timeInterval)
my_data['timeinterval']=timeInterval
overThirty=my_data[my_data["timeinterval"]>1800]#与上一个航班超过30分钟的
service.putData("overThirty",overThirty)
# print(overTime)
# my_data['timeinterval'].plot()
# xaxis=np.arange(18000)
# thirty=np.array([1800 for i in range(18000)])
# plt.plot(xaxis,thirty)
# plt.show()



print(overThirty)