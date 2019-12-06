
from sqlalchemy import create_engine
import pandas as pd

class SqlHelper(object):
    db_info = {'user': 'root',
               'password': '123456',
               'host': '39.97.177.49',
               'database': 'testWfj'
               }
    db_info1 = {'user': 'newairportjd',
               'password': '`1qazx',
               'host': '220.163.112.108',
               'database': 'newairport'
               }

    mysql_cn = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s/%(database)s?charset=utf8' % db_info)  # 这里直接使用pymysql连接
    # mysql_cn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='airport_plane')


    def getData(self,type,carId="",startTime="",endTime=""):
        if(type=="possible points"):
            sql = "SELECT CONCAT(a.lng, ',', a.lat) AS positionIndex,	TIMESTAMPDIFF(MINUTE,MIN(gps_time),MAX(gps_time)) AS timeHere FROM ( SELECT gps_time,lng,lat,acc_status from car_gps_2019_04  union all SELECT gps_time,lng,lat,acc_status  FROM car_gps_2019_05 ) a WHERE a.gps_time>'2019-04-01 00:00:00' and  a.gps_time<'2019-06-01 00:00:00' AND a.acc_status = '0' GROUP BY CONCAT(a.lng, ',', a.lat) HAVING timeHere>0 ORDER BY timeHere DESC"
        elif (type=="departure"):
            sql = "select * from deptflt1 where fatd > '2019-04-01 00:00:00'AND fatd < '2019-05-01 00:00:00'ORDER BY fatd"
        elif(type=='jwbh'):
            sql="SELECT * FROM jwbh WHERE jwbh>'300'"
        elif(type=="parkingPoints"):
            sql="SELECT possible_points_b.indexs,possible_points_b.lng,possible_points_b.lat FROM possible_points_b,beusedpossiblepoints WHERE possible_points_b.indexs=beusedpossiblepoints.indexs"
            # sql="SELECT * FROM  possible_points WHERE  indexs!='25' and indexs !='83' and indexs!='95' and indexs !='120'  ORDER BY timeHere DESC LIMIT 0,180"
        elif(type=="showPosilePoints"):
            sql="SELECT * FROM possible_points ORDER BY timeHere DESC LIMIT 0,180"

        # 进行时间挖掘过程中用到的4月5月两个月的数据
        elif(type=="oneCarRouts"):
            sql="SELECT a.gps_time, a.lng, a.lat ,a.speed FROM \
            ( SELECT max(gps_time) as gps_time ,lng ,lat ,speed FROM car_gps_2019_04 WHERE vehicle_id = '%s' GROUP BY CONCAT(lng, ',', lat) UNION ALL SELECT max(gps_time) as gps_time ,lng ,lat,speed FROM car_gps_2019_05\
             WHERE vehicle_id = '%s' GROUP BY CONCAT(lng, ',', lat)) a\
             WHERE a.gps_time>'%s' and a.gps_time<'%s'\
             ORDER By a.gps_time"%(carId,carId,startTime,endTime)


        elif(type=="shuttlBus"):
            sql="SELECT * FROM shuttlBus"
        elif(type=="gateNum"):#远机位
            sql="SELECT jwbh,lng,lat FROM gate_num WHERE SUBSTR(jwbh,1,3)>300"
        elif(type=="boarding_num"):#登机口
            sql="SELECT * FROM boarding_gate"
        elif(type=="parkPoint"):
            sql="SELECT * FROM parking_point"
        elif(type=="car_id"):
            sql="SELECT * FROM car_id"
        elif(type=="oneCarOnTime"):
            self.mysql_cn = create_engine(
                'mysql+pymysql://%(user)s:%(password)s@%(host)s/%(database)s?charset=utf8' % self.db_info1)  # 这里直接使用pymysql连接
            sql = "SELECT max(gps_time) as gps_time ,lng ,lat ,speed FROM car_gps_{start1}_{start2} WHERE vehicle_id = {vehicle_id} and gps_time>'{start3}' and gps_time<'{endd}' GROUP BY CONCAT(lng, ',', lat)  ORDER BY gps_time " .format(start1=startTime[0:4],start2=startTime[5:7],start3=startTime,endd=endTime,vehicle_id=carId)
        # 从arraft表里面获取数据获取字段fsta预计到达时间
        elif(type=="arraft_fsta"):
            sql="SELECT DISTINCT(CONCAT(YEAR(fsta),MONTH(fsta),DAY(fsta),'|',fflt)), fsta FROM arrvflt WHERE fsta>'%s' and fsta<'%s' ORDER BY fsta"%(startTime,endTime)
        elif(type=="arraveData"):
            sql="SELECT air_crft_reg_nbr,	airln_cd,	arrv_dt,	dpt_dt,	estmt_arrv_dt,	estmt_dpt_dt,	schd_arrv_dt,	schd_dpt_dt	,dep_cty_chn_nm,	arrv_cty_chn_nm FROM xml_flight_info_backUp WHERE arrv_dt > '%s' AND arrv_dt < '%s' ORDER BY arrv_dt"%(startTime,endTime)
            print(sql)
        my_data = pd.read_sql(sql, con=self.mysql_cn)
        return my_data

    # 触地时间
    def getFtdtByJwbh(self,bh):
        sql="SELECT fatd FROM deptflt1 WHERE jwbh ='%s' and  fatd >'2019-04-01 00:00:00' and  fatd <'2019-06-01 00:00:00' ORDER BY fatd"%(bh)
        data=pd.read_sql(sql,con=self.mysql_cn)
        return data
    def getCarsByTime(self,start,end):
        sql = "SELECT 	CONCAT(lng, ',', lat) AS positionIndex FROM 	car_gps_2019_04  WHERE 	gps_time > '%s' AND gps_time < '%s' AND acc_status = '0' GROUP BY  	CONCAT(lng, ',', lat) "%(start,end)
        data=pd.read_sql(sql,con=self.mysql_cn)
        return  data
    def putData(self,name,data_frame):

        data_frame.to_sql(name,con=self.mysql_cn,if_exists='replace',chunksize=100)
    def closResouce(self):
        return self.mysql_cn.dispose()




# def doSql(sql):
#     mysql_cn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='airport_plane')
#     my_data=pd.read_sql(sql,con=mysql_cn)
#     mysql_cn.close()
#     return my_data


