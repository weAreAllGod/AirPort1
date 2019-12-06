import requests
import pandas as pd
import json
requestData=requests.get("http://api.k780.com/?app=weather.city&cou=1&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json")
jsonData=requestData.json()
codeList=[]
provinceList=[]
cityList=[]
districtList=[]
weNeedList=[]
for data in jsonData["result"]["datas"]:
    code=data
    province=jsonData["result"]["datas"][str(code)]["area_1"]
    city=jsonData["result"]["datas"][str(code)]["area_2"]
    district=jsonData["result"]["datas"][str(code)]["citynm"]
    # nm=jsonData["result"]["datas"][str(code)]["area_3"]
    codeList.append(code)
    provinceList.append(province)
    cityList.append(city)
    districtList.append(district)
codeAndCityDataF=pd.DataFrame(columns=["code","province","city","district"])
codeAndCityDataF["code"]=pd.Series(codeList)
codeAndCityDataF["province"]=pd.Series(provinceList)
codeAndCityDataF["city"]=pd.Series(cityList)
codeAndCityDataF["district"]=pd.Series(districtList)

codeAndCityDataF.to_csv("../state/data/anlysisForDelay/cityAndCode.csv",encoding="gbk")
