import webbrowser
from webbrowser import Chrome
import pandas as pd
import requests
import json
def showInBrow(Datas,infor,template):
    lng = []
    lat = []
    label = []
    for index, value in Datas.iterrows():
        # print("-------------->没转化的时候",value['index'])
        url = "http://api.map.baidu.com/geoconv/v1/?"
        url += "coords=%s,%s" % (value['lng'], value['lat'])
        url += "&from=1&to=5&ak=iDGvjjogGZch7Gf8tPAhxTv6GnQEw9Tn"
        result = requests.get(url)
        result = json.loads(result.text)
        if (result["status"] == 0):
            # print("------------------>转化后",value["index"])
            if (infor=="lng+lat"):
                label.append(str(value['lng']) + "," + str(value["lat"]))
            elif(infor=="gps_time"):
                label.append(str(value['gps_time']))
            elif(infor=="pointName"):
                label.append(str(value['pointName']))
            elif(infor=="vehicle_id"):
                label.append(str(value['vehicle_id']))
            elif(infor=="vehicleAndTime"):
                label.append(str(value['vehicle_id'])+"车"+str(value['gps_time']))



            lng.append(result["result"][0]["x"])
            lat.append(result["result"][0]["y"])
        else:
            print("第%s坐标转化出现了错误" % (index + 1))
        # print(resutl["result"][0]["x"],resutl["result"][0]["y"])
    # 选择前多少行进行展示
    showDatas=pd.DataFrame(columns=["lng","lat","label"])
    showDatas['lng'] = pd.Series(lng)
    showDatas['lat'] = pd.Series(lat)
    showDatas['label'] = pd.Series(label)

    pointStr = ""
    for index, value in showDatas.iterrows():
        pointStr += "[new BMap.Point(%s,%s),%s],\n" % (value['lng'], value['lat'], [value['label']])


    f=open("../state/%s.html"%(template),encoding='utf-8')
    html=""
    if template=="allPointsTemplate":
        lineNeeded=204
    else:
        lineNeeded=17
    i=0
    for line in f:
        i+=1
        if (i==lineNeeded):
            html+="var points = [%s];\n"%(pointStr)
        html+=line
    f.close()

    f1=open("../state/showData.html",'w',encoding='utf-8')
    f1.write(html)
    f1.close()
    # webbrowser.register('chrome', Chrome('chrome'))
    webbrowser.open('E:\Projects\AirPort\state\showData.html')
    # print(html)
