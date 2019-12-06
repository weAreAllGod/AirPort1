from dataProcessing import mapper

def getData(type,carId="",startTime="",endTime=""):
    sql_helper=mapper.SqlHelper()
    my_data=sql_helper.getData(type,carId,startTime,endTime)
    sql_helper.closResouce()
    return my_data
def putData(name,dataFrame):
    sql_helper = mapper.SqlHelper()
    sql_helper.putData(name,dataFrame)
    sql_helper.closResouce()
    return "导入操作成功"
def getFtdtByJwbh(bh):
    sql_helper = mapper.SqlHelper()
    fgots=sql_helper.getFtdtByJwbh(bh)
    sql_helper.closResouce()
    return fgots
def getCarsByTime(start,end):
    sql_helper = mapper.SqlHelper()
    cars = sql_helper.getCarsByTime(start,end)
    sql_helper.closResouce()
    return cars


