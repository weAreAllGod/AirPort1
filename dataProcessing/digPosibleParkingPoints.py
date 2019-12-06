import numpy as np
import pandas as pd
from  dataProcessing import service
from  dataProcessing import showData
import requests
import json



rowData=service.getData("possible points")
myData=pd.DataFrame(columns=['lng','lat','timeHere'])

columnsList=rowData.columns.tolist()
#如果是个性化的操作，比如统计地点频率
if ("positionIndex" in columnsList):
    columnsList.append('lng')
    columnsList.append('lat')
    rowData.reindex(columns=columnsList)
    rowData['lng']=rowData['positionIndex'].apply(lambda x:x.split(',')[0])
    rowData['lat']=rowData['positionIndex'].apply(lambda x:x.split(',')[1])
    rowData['lng']=rowData['lng'].astype('float')
    rowData['lat']=rowData['lat'].astype('float')
    rowData['timeHere']=rowData['timeHere'].astype('float')
    # 需要对区域内的数据进行合并去除重复的点
    boudary=30/111000
    po_pa_po=[]
    for index,value in rowData.iterrows():
        if index==0:
            po_pa_po.append([value['lng'], value['lat'],value['timeHere']])
        else:
            count=0
            for item in po_pa_po:
                if np.abs(item[0] - value['lng']) < boudary and np.abs(item[1] - value['lat'] )< boudary:
                    item[2]+=value['timeHere']
                    break
                else:
                    count+=1
                    continue
            if count==len(po_pa_po):
                po_pa_po.append([value['lng'], value['lat'],value['timeHere']])
    po_pa_po=np.array(po_pa_po)
    myData['lng'] = pd.Series(po_pa_po[:,0])
    myData['lat'] = pd.Series(po_pa_po[:,1])
    myData['timeHere']=pd.Series(po_pa_po[:,2])
else:
    myData['lng'] = rowData['lng'].astype('float')
    myData['lat'] = rowData['lat'].astype('float')


# 对坐标在一个区域内的进行处理
service.putData("possible_points",myData)
# 坐标转化并展示在百度地图上这里的showData只显示打分最高的前200个数
showDatas=service.getData("showPosilePoints")

showData.showInBrow(showDatas,infor="lng+lat",template="template")

    



