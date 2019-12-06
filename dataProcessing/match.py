from dataProcessing import service
import pandas as pd
import numpy as np

def getMaxIndexs(arra):
    maxIndexs=[arra.argmax()]
    for i in range(arra.argmax()+1,len(arra)):
        if arra[i]==arra[arra.argmax()]:
            maxIndexs.append(i)

jwbh=service.getData('jwbh')
boudary=30/111000
allPossiblePoints=service.getData("parkingPoints")
match=pd.DataFrame(columns=['jwbh','indexs'])
temp_jw=[]
temp_in=[]
for index,value in jwbh.iterrows():
    # 该机位所有的开仓们的时间
    print(index)
    fgots = service.getFtdtByJwbh(value['jwbh'])
    goats={}
    for index1 ,value1 in fgots.iterrows():
        endTime=value1['fatd']
        startTime=endTime-pd._libs.tslibs.timestamps.Timedelta('0 days 00:15:00')
        carsPoints=service.getCarsByTime(startTime,endTime)
        for index2,value2 in carsPoints.iterrows():
            for index3,value3 in allPossiblePoints.iterrows():
                if np.abs(float(value2['positionIndex'].split(',')[0])-float(value3['lng']))<boudary and np.abs(float(value2['positionIndex'].split(',')[1])-float(value3['lat']))<boudary:
                    if value3['indexs'] not in goats:
                        goats[value3['indexs']]=1
                    else:
                        goats[value3['indexs']]+=1
                    break
    temp_jw.append(value['jwbh'])
    temp_in.append(max(goats,key=goats.get))
    print(value['jwbh'],max(goats,key=goats.get))
    print(goats)
match['jwbh']=pd.Series(temp_jw)
match['indexs']=pd.Series(temp_in)
match.to_csv('match.csv')
print(match)








# print(fgots)