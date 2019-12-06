# -*- coding: cp936 -*-
# -*- coding:utf-8 -*-
##按空间分割，先对近机位（分成国内，国际两种机位分别进行分配）分配，更新机位空闲时间，再分配远机位
#在建立航班和机位list时     要分为国际航班的list,国内航班list     要分为国内机位（近机位list,远机位list）以及国际机位（近机位list,远机位list）
##下一步再按照机型分类
import time
time1=time.asctime(time.localtime(time.time()))
#目前手工输入分配日期，应该写在发送data的文件开头
assigntime='2017/06/03 00:00'
# final_starttime='2017/04/10 00:00'
# final_endtime='2017/04/12 00:00'
# 时间转换函数（到分钟）
def timed(a):
    timeArray = time.strptime(a, "%Y/%m/%d %H:%M")
    timeStamp = int(time.mktime(timeArray)) / 60
    return timeStamp
# 分钟浮点数转换成标准时间函数
def datetimed(a):
    timeTuple = time.localtime(a*60)
    timeArray=time.strftime('%Y/%m/%d %H:%M',timeTuple)
    return timeArray

final_starttime=datetimed(timed(assigntime)-1440*2) #分配日期前48小时
final_endtime=datetimed(timed(assigntime)+1440*2) #分配日期后48小时


# 时间转换为标准日期格式
# import time
# def timestandard(a):
#     day_now = time.localtime()
#     fulldate='%s(%d%02d%s)' %(a[0:4],day_now.tm_year, day_now.tm_mon,a[5:7])
#     timeArray = time.strptime(fulldate, "%H%M(%Y%m%d)")
#     timeStandard = time.strftime("%Y/%m/%d %H:%M", timeArray)
#     return timeStandard

#更改月份五月！
def timestandard(a):
    day_now = time.localtime()
    fulldate='%s(%d06%s)' %(a[0:4],day_now.tm_year,a[5:7])
    timeArray = time.strptime(fulldate, "%H%M(%Y%m%d)")
    timeStandard = time.strftime("%Y/%m/%d %H:%M", timeArray)
    return timeStandard

##1.定义flight类
class flight:
    def __init__(self,flightid,aflightno,dflightno,flightnum,atime,dtime,paras,mdl,nation,apassenger,dpassenger,arrive,departure,gate):
        self.flightid=flightid
        self.aflightno=aflightno
        self.dflightno=dflightno
        self.flightnum=flightnum
        self.atime=atime
        self.dtime=dtime
        self.intatime=timed(atime)
        self.intdtime=timed(dtime)
        self.paras=paras
        self.mdl=mdl
        self.nation=nation
        self.apassenger=apassenger
        self.dpassenger = dpassenger
        self.arrive=arrive
        self.departure=departure
        self.gate=gate
        self.pro_gate=gate

##2.定义gate类
class Gate:
    def __init__(self,gateno,mdl,nation,bridge,starttime,endtime):
        self.gateno=gateno
        self.mdl=mdl
        self.nation=nation
        self.bridge=bridge
        self.starttime=starttime
        self.endtime=endtime
        self.flightset=[]
    ##定义类方法：把航班添加进其对应的航班计划flightset中
    def getflight(self,flight):
        if flight.gate==self.gateno:
            self.flightset.append(flight)
    ##定义类方法（寻找空闲时间）
    ##先对flightset中的航班对象排序，按照航班的到达时间由小到大排序，然后依次获得空闲时间
    def findresttime(self):
        flightset=self.flightset
        try:
            import operator
        except ImportError:
            cmpfun = lambda x: x.count  # use a lambda if no operator module
        else:
            cmpfun = operator.attrgetter('intatime')  # use operator since it's faster than lambda
        flightset.sort(key=cmpfun)
        #初始化时，    starttime = [final_starttime]、 endtime = [final_endtime]
        if type(self.starttime)==str:
            final_starttime=self.starttime
        else:
            final_starttime = self.starttime[0]

        self.starttime=[]
        self.endtime=[]
        if len(flightset)<1:
            self.starttime.append(final_starttime)
            self.endtime.append(final_endtime)
        else:
            for i in range(len(flightset)+1):
                if i==0:
                    self.starttime.append(final_starttime)
                    self.endtime.append(flightset[i].atime)
                elif i==len(flightset):
                    self.starttime.append(flightset[i-1].dtime)
                    self.endtime.append(final_endtime)
                else:
                    self.starttime.append(flightset[i-1].dtime)
                    self.endtime.append(flightset[i].atime)

###3.初始化航班和机位数据
assignment = open("0603ad-csv.csv", 'r')
next(assignment)  # 跳过第一行表头，从第二行开始读数据
jstr_flight = []
id=0
for line in assignment:
    line = line.rstrip().split(',')
    if line[0]!='':
        jstr_flight.append({'flightid': str(id), 'aflightno': line[0], 'dflightno': line[1], 'flightnum': line[2], 'atime': line[3],
                   'dtime': line[4], 'paras': line[5], 'mdl': line[6], 'gate': line[7],
                   'nation': line[8], 'apassenger': line[9], 'dpassenger': line[10]})
        id=id+1

# 读机位数据csv，写入list ，数据格式为[{item1:xx,item2:xx},{item1:xx,item2:xx}]
gatedata = open("gate-csv.csv", 'r')
next(gatedata)  # 跳过第一行表头，从第二行开始读数据
jstr_gate = []
for line in gatedata:
    line = line.rstrip().split(',')
    jstr_gate.append({'gateno': line[0], 'mdl': line[1], 'nation': line[2], 'bridge': line[3], 'starttime': line[4]})

#读取国际航班标识数据
f = open("nation.txt","r")
lines = f.readlines()
nation=[]
for line in lines:
    line=line.strip('\n')
    nation.append(line)

bridge_gatenum=0
##添加修改航班属性值
for i in range(len(jstr_flight)):
    if jstr_flight[i]['gate'][0]=='1':
        bridge_gatenum =bridge_gatenum+1
    ##更改时间格式为标准格式
    jstr_flight[i]['atime']=timestandard(jstr_flight[i]['atime'])
    jstr_flight[i]['dtime'] = timestandard(jstr_flight[i]['dtime'])
    ##将flight数据中机型数据改为数值
    if jstr_flight[i]['mdl'][-1]=='C':
        jstr_flight[i]['mdl'] = 3
    elif jstr_flight[i]['mdl'][-1] == 'D':
        jstr_flight[i]['mdl'] = 4
    elif jstr_flight[i]['mdl'][-1] == 'E':
        jstr_flight[i]['mdl'] = 5
    else:
        jstr_flight[i]['mdl'] = 6
     ##flight数据 添加paras、arrive、departure、nation属性
    if timed(jstr_flight[i]['atime'])<timed(assigntime) and timed(jstr_flight[i]['dtime'])>timed(assigntime) :
        jstr_flight[i]['paras']='1'
        jstr_flight[i]['arrive']='1'
        jstr_flight[i]['departure'] = '0'
    else:
        jstr_flight[i]['paras'] = '0'
        jstr_flight[i]['gate']='0'
        jstr_flight[i]['arrive']='0'
        jstr_flight[i]['departure'] = '0'
    if jstr_flight[i]['aflightno'][0:2] in nation:
        jstr_flight[i]['nation']='1'
    else:jstr_flight[i]['nation']='0'

for i in range(len(jstr_flight)):
    flightid = jstr_flight[i]['flightid']
    aflightno = jstr_flight[i]['aflightno']
    dflightno = jstr_flight[i]['dflightno']
    flightnum=jstr_flight[i]['flightnum']
    atime = jstr_flight[i]['atime']
    dtime = jstr_flight[i]['dtime']
    paras = jstr_flight[i]['paras']
    mdl = jstr_flight[i]['mdl']
    gate = jstr_flight[i]['gate']
    nation = jstr_flight[i]['nation']
    apassenger = jstr_flight[i]['apassenger']
    dpassenger = jstr_flight[i]['dpassenger']
    # arrive=jstr_flight[i]['arrive']
    # departure=jstr_flight[i]['departure']
    print (flightid, aflightno, dflightno, flightnum,atime, dtime, paras, mdl, nation, apassenger, dpassenger,gate)#arrive,departure,


##将gate数据中机型数据改为数值
for i in range(len(jstr_gate)):
    if jstr_gate[i]['mdl'] == 'C':
        jstr_gate[i]['mdl'] = 3
    elif jstr_gate[i]['mdl'] == 'D':
        jstr_gate[i]['mdl'] = 4
    elif jstr_gate[i]['mdl'] == 'E':
        jstr_gate[i]['mdl'] = 5
    else:
        jstr_gate[i]['mdl'] = 6
    # 修改中文国际国内属性为0、1
    if jstr_gate[i]['nation']=='国际':
        jstr_gate[i]['nation']='1'
    else:
        jstr_gate[i]['nation'] ='0'
        # 修改中文国际国内属性为0、1
    if jstr_gate[i]['bridge'] == '1':
        jstr_gate[i]['bridge'] = '2'
    else:
        jstr_gate[i]['bridge'] = '1'
######################################################################################################################################
##产生internal_flightlist国内航班集合，以及external_flightlist国际航班集合，包含flight对象
internal_flightlist_C=[]
internal_flightlist_D=[]
internal_flightlist_E=[]
internal_flightlist_F=[]
external_flightlist_C=[]
external_flightlist_D=[]
external_flightlist_E=[]
external_flightlist_F=[]
##停放在近机位，不能进行拖曳，作为已分配航班不参与机位分配，仅参与摆渡车分配
human_assign_list = []
for i in range(len(jstr_flight)):
    if jstr_flight[i]['paras'] == '1' and (jstr_flight[i]['gate'][0] != '3' and jstr_flight[i]['gate'][0] != '5' and jstr_flight[i]['gate'][0] != '7' and jstr_flight[i]['gate'][0] != 'L'):
        flightid = jstr_flight[i]['flightid']
        aflightno = jstr_flight[i]['aflightno']
        dflightno = jstr_flight[i]['dflightno']
        flightnum = jstr_flight[i]['flightnum']
        atime = jstr_flight[i]['atime']
        dtime = jstr_flight[i]['dtime']
        paras = jstr_flight[i]['paras']
        mdl = jstr_flight[i]['mdl']
        nation = jstr_flight[i]['nation']
        apassenger = jstr_flight[i]['apassenger']
        dpassenger = jstr_flight[i]['dpassenger']
        arrive=jstr_flight[i]['arrive']
        departure=jstr_flight[i]['departure']
        gate = jstr_flight[i]['gate']
        flt = flight(flightid, aflightno, dflightno, flightnum,atime, dtime, paras, mdl, nation, apassenger, dpassenger,arrive,departure, gate)
        human_assign_list.append(flt)
        continue
    ##需要进行分配的航班(包括没有机位的航班以及分配到远机位的单进航班对)
    else:# 已进港的远机位和未进港
        flightid = jstr_flight[i]['flightid']
        aflightno = jstr_flight[i]['aflightno']
        dflightno = jstr_flight[i]['dflightno']
        flightnum = jstr_flight[i]['flightnum']
        paras = jstr_flight[i]['paras']
        atime = jstr_flight[i]['atime']
        dtime = jstr_flight[i]['dtime']
        mdl = jstr_flight[i]['mdl']
        nation = jstr_flight[i]['nation']
        apassenger = jstr_flight[i]['apassenger']
        dpassenger = jstr_flight[i]['dpassenger']
        arrive=jstr_flight[i]['arrive']
        departure=jstr_flight[i]['departure']
        gate = jstr_flight[i]['gate']
        flt = flight(flightid, aflightno, dflightno,flightnum, atime, dtime, paras, mdl, nation, apassenger, dpassenger,
                     arrive, departure, gate)
        if flt.nation=='1':
            if flt.mdl==3:
                external_flightlist_C.append(flt)
            elif flt.mdl==4:
                external_flightlist_D.append(flt)
            elif flt.mdl==5:
                external_flightlist_E.append(flt)
            else:
                external_flightlist_F.append(flt)
        else:
            if flt.mdl==3:
                internal_flightlist_C.append(flt)
            elif flt.mdl==4:
                internal_flightlist_D.append(flt)
            elif flt.mdl==5:
                internal_flightlist_E.append(flt)
            else:
                internal_flightlist_F.append(flt)

# 建立所有机位的对象集合
allgatelist = []
for i in range(len(jstr_gate)):
    gateno = jstr_gate[i]['gateno']
    mdl = jstr_gate[i]['mdl']
    nation = jstr_gate[i]['nation']
    bridge = jstr_gate[i]['bridge']
    starttime = [final_starttime]
    endtime = [final_endtime]
    gt = Gate(gateno, mdl, nation, bridge, starttime, endtime)
    allgatelist.append(gt)
    # for j in human_assign_list:
    #     gt.getflight(j)
    # gt.findresttime()
    # # print(gt.gateno,gt.starttime,gt.endtime)

# 远机位对象集合????????????
# apron=[]
# for i in range(len(allgatelist)):
#     if allgatelist[i].bridge=='0':
#         apron.append(i)
# print(apron)
remotegate = []
for i in range(len(allgatelist)):
    if allgatelist[i].bridge == '0':
        remotegate.append(allgatelist[i].gateno)
        # print (remotegate)

#################################################################################################################################
##产生gatelist,包含gate对象
external_apron_gatelist_C=[]##国际远机位
external_apron_gatelist_D=[]##国际远机位
external_apron_gatelist_E=[]##国际远机位
external_apron_gatelist_F=[]##国际远机位
external_near_gatelist_C=[]##国际近机位
external_near_gatelist_D=[]##国际近机位
external_near_gatelist_E=[]##国际近机位
external_near_gatelist_F=[]##国际近机位
internal_apron_gatelist_C=[]##国内远机位
internal_apron_gatelist_D=[]##国内远机位
internal_apron_gatelist_E=[]##国内远机位
internal_apron_gatelist_F=[]##国内远机位
internal_near_gatelist_C=[]##国内近机位
internal_near_gatelist_D=[]##国内近机位
internal_near_gatelist_E=[]##国内近机位
internal_near_gatelist_F=[]##国内近机位
##根据机位的国际国内属性，是否拥有廊桥及可容纳机型将机位对象分别放入不同的机位集合中
for i in range(len(jstr_gate)):
    gateno = jstr_gate[i]['gateno']
    mdl = jstr_gate[i]['mdl']
    nation = jstr_gate[i]['nation']
    bridge = jstr_gate[i]['bridge']
    starttime = [final_starttime]
    endtime = [final_endtime]
    gt=Gate(gateno,mdl,nation,bridge,starttime,endtime)
    ##对每个机位而言，更新其初始空闲时间
    ##将不参与分配的航班分配至机位flightset中，并进一步更新初始机位空闲时间
    for j in human_assign_list:
        gt.getflight(j)
    gt.findresttime()
    print(gt.gateno,gt.starttime,gt.endtime,gt.mdl)

    ##国际
    if gt.nation == '1':
        ##国际有廊桥
        if gt.bridge == '2':
            if gt.mdl == 3:
                external_near_gatelist_C.append(gt)
            elif gt.mdl == 4:
                external_near_gatelist_D.append(gt)
            elif gt.mdl == 5:
                external_near_gatelist_E.append(gt)
            else:
                external_near_gatelist_F.append(gt)
        ##国际没有廊桥
        else:
            if gt.mdl == 3:
                external_apron_gatelist_C.append(gt)
            elif gt.mdl == 4:
                external_apron_gatelist_D.append(gt)
            elif gt.mdl == 5:
                external_apron_gatelist_E.append(gt)
            else:
                external_apron_gatelist_F.append(gt)
    else:
        ##国内有廊桥
        if gt.bridge == '2':
            if gt.mdl == 3:
                internal_near_gatelist_C.append(gt)
            elif gt.mdl == 4:
                internal_near_gatelist_D.append(gt)
            elif gt.mdl == 5:
                internal_near_gatelist_E.append(gt)
            else:
                internal_near_gatelist_F.append(gt)
        ##国内没有廊桥
        else:
            if gt.mdl == 3:
                internal_apron_gatelist_C.append(gt)
            elif gt.mdl == 4:
                internal_apron_gatelist_D.append(gt)
            elif gt.mdl == 5:
                internal_apron_gatelist_E.append(gt)
            else:
                internal_apron_gatelist_F.append(gt)
                ###开始进行分配
##############################################################################################################################
##定义求解函数
import pulp
def gate_assignment_model(flightlist,gatelist):
    assigned_apron_flights=[]
    for i in range(len(flightlist)):
        if flightlist[i].paras=='1' and (flightlist[i].pro_gate[0]=='3' or flightlist[i].pro_gate[0]=='5' or flightlist[i].pro_gate[0]=='7' or flightlist[i].pro_gate[0]=='L'):
            assigned_apron_flights.append(i)

    apron=[]
    for i in range(len(gatelist)):
        if gatelist[i].bridge=='1':
            apron.append(i)

    # 构造Q矩阵（判断机位机型匹配以及国际国内属性匹配）！！认为mdl为机型，people为国际国内属性,且均为字符串类型 ，可以停靠1，不可以0.
    Q = {}
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            if (int(gatelist[k].mdl) - int(flightlist[i].mdl)) >= 0 and int(flightlist[i].nation) == int(gatelist[k].nation):
                Q[(i, k)] = 1
            else:
                Q[(i, k)] = 0

    print('Q矩阵处理完毕##################################################')

    # 定义函数判断时间是否冲突isTimeCollision
    def isTimeCollision(a, b, c, d):
        if (b > c and b <= d) or (d > a and d <= b):
            return 1
        elif (a >= c and a < d) or (c >= a and c < b):
            return 1
        else:
            return 0

    # 开始构造T矩阵（判断两航班机位占用时间是否冲突，左右各加Tb/2） 冲突1 ，不冲突0.
    Tb = 10
    T = {}
    for i in range(len(flightlist)):
        for j in range(len(flightlist)):
            if i != j:
                flt1_atime = flightlist[i].intatime
                flt1_dtime = flightlist[i].intdtime
                flt2_atime = flightlist[j].intatime
                flt2_dtime = flightlist[j].intdtime
                if isTimeCollision(flt1_atime - Tb / 2, flt1_dtime + Tb / 2, flt2_atime - Tb / 2,
                                   flt2_dtime + Tb / 2) == 1:
                    T[(i, j)] = 1
                else:
                    T[(i, j)] = 0
            else:
                T[(i, j)] = 0

    print('T矩阵处理完毕###########################################################')
    # 开始构造Z矩阵(空闲时间段) 航班时间属于机位空闲时间段内1，不属于0
    Z = {}
    for i in range(len(flightlist)):
        flt_atime = flightlist[i].intatime
        flt_dtime = flightlist[i].intdtime
        for k in range(len(gatelist)):
            belong = 0
            for ii in range(len(gatelist[k].starttime)):
                gate_starttime = timed(gatelist[k].starttime[ii])
                gate_endtime = timed(gatelist[k].endtime[ii])
                if (flt_atime >= gate_starttime + 10) & (flt_dtime <= gate_endtime - 10):
                    belong = belong + 1
            if belong >= 1:
                Z[(i, k)] = 1
            else:
                Z[(i, k)] = 0


    # 构造函数，两矩阵合并，键值取小
    def union(d1, d2):
        repeat = [i for i in d1.keys() if i in d2.keys()]
        d3 = {}
        for i in repeat:
            d3[i] = min(d1[i], d2[i])
        return (d3)
    print('开始求解###################################################')
    prob = pulp.LpProblem('selection', pulp.LpMaximize)
    vars = {}
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            vars[(i, k)] = pulp.LpVariable('%d_%s' % (i, k), lowBound=0, cat='Integer')
    # # 建立目标函数（最大化分配至近机位的航班数量）
    # m.setObjective(quicksum(x[i, k] * int(gatelist[k].bridge) for i, k in arcs),
    #                GRB.MAXIMIZE)
    prob += sum(vars[(i, k)] * int(gatelist[k].bridge) for i, k in vars.keys())
    # 添加各项约束
    ## 匹配性约束：针对Q，Z矩阵
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            if union(Q, Z)[i, k] == 0:
                prob += vars[(i, k)] == 0
    ##每个航班最多分配一个机位（约束放松）
    for i in range(len(flightlist)):
        prob += sum(vars[(i, k)] for k in range(len(gatelist))) <= 1
    ##机位占用时间冲突的航班不能分配至同一个机位
    for k in range(len(gatelist)):
        for i in range(len(flightlist)):
            for j in range(len(flightlist)):
                if T[i, j] == 1:
                    prob += vars[(i, k)] + vars[(j, k)] <= 1
    ##对于可拖曳航班（已分配航班且分配至远机位），仅能重新分配至近机位或者保持其机位不变
    for i in assigned_apron_flights:
        for k in apron:
            if flightlist[i].pro_gate==gatelist[k].gateno:
                for kk in apron:
                    if kk != k:
                        prob += vars[(i, kk)] == 0
    # 求解问题写入test_1.py文件中
    prob.writeLP('test_1.lp')

    # 求解
    print('开始时间：', time.asctime(time.localtime(time.time())))
    prob.solve()
    print('结束时间：', time.asctime(time.localtime(time.time())))
    # 打印结果
    print('optimize_status: %s' % pulp.LpStatus[prob.status])
    print('var_list:')
    for i in prob.variables():
        # print(i,type(i))
        if i.varValue != 0:
            print('    %s = %s' % (i.name, i.varValue))
    ##定义已分配航班集合
    assigned_flightlist=[]
    for i in prob.variables():
        if i.varValue != 0:
            result=i.name.split('_')
            flightlist[int(result[0])].gate = gatelist[int(result[1])].gateno
            assigned_flightlist.append(i)
            #print(flightlist[int(result[0])].aflightno,flightlist[int(result[0])].destination, flightlist[int(result[0])].atime, flightlist[int(result[0])].dtime,
            #     flightlist[int(result[0])].ParkingGate)

    print('total_value: %d' % pulp.value(prob.objective))
    ##若可拖曳航班在此次分配中未分配机位，则将其gate属性设置为0
    for i in assigned_apron_flights:
        if i not in assigned_flightlist:
            flightlist[i].gate='0'
################################################################################################################################
##定义求解函数
def gate_assignment_model_strict(flightlist, gatelist):
    assigned_apron_flights = []
    for i in range(len(flightlist)):
        if flightlist[i].paras == '1' and (
                        flightlist[i].pro_gate[0] == '3' or flightlist[i].pro_gate[0] == '5' or flightlist[i].pro_gate[0] == '7' or
                flightlist[i].pro_gate[0] == 'L'):
            assigned_apron_flights.append(i)

    apron = []
    for i in range(len(gatelist)):
        if gatelist[i].bridge == '1':
            apron.append(i)

    # 构造Q矩阵（判断机位机型匹配以及国际国内属性匹配）！！认为mdl为机型，people为国际国内属性,且均为字符串类型
    Q = {}
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            if (int(gatelist[k].mdl) - int(flightlist[i].mdl)) >= 0 and int(flightlist[i].nation) == int(
                    gatelist[k].nation):
                Q[(i, k)] = 1
            else:
                Q[(i, k)] = 0

    print('Q矩阵处理完毕############################机型可以停靠1，不可以0.######################')
    print (Q)

    # 定义函数判断时间是否冲突isTimeCollision
    def isTimeCollision(a, b, c, d):
        if (b > c and b <= d) or (d > a and d <= b):
            return 1
        elif (a >= c and a < d) or (c >= a and c < b):
            return 1
        else:
            return 0

    # 开始构造T矩阵（判断两航班机位占用时间是否冲突，左右各加Tb/2）
    Tb = 10
    T = {}
    for i in range(len(flightlist)):
        for j in range(len(flightlist)):
            if i != j:
                flt1_atime = flightlist[i].intatime
                flt1_dtime = flightlist[i].intdtime
                flt2_atime = flightlist[j].intatime
                flt2_dtime = flightlist[j].intdtime
                if isTimeCollision(flt1_atime - Tb / 2, flt1_dtime + Tb / 2, flt2_atime - Tb / 2,flt2_dtime + Tb / 2) == 1:
                    T[(i, j)] = 1
                else:
                    T[(i, j)] = 0
            else:
                T[(i, j)] = 0

    print('T矩阵处理完毕#############################两航班机位占用时间 冲突1 ，不冲突0.##############################')
    print (T)
    # 开始构造Z矩阵(空闲时间段)
    Z = {}
    for i in range(len(flightlist)):
        flt_atime = flightlist[i].intatime
        flt_dtime = flightlist[i].intdtime
        for k in range(len(gatelist)):
            belong = 0
            for ii in range(len(gatelist[k].starttime)):
                gate_starttime = timed(gatelist[k].starttime[ii])
                gate_endtime = timed(gatelist[k].endtime[ii])
                if (flt_atime >= gate_starttime + 10) & (flt_dtime <= gate_endtime - 10):
                    belong = belong + 1
            if belong >= 1:
                Z[(i, k)] = 1
            else:
                Z[(i, k)] = 0
    print('Z矩阵处理完毕##############航班时间属于机位空闲时间段内1，不属于0.##############################')
    print (Z)


    # 构造函数，两矩阵合并，键值取小
    def union(d1, d2):
        repeat = [i for i in d1.keys() if i in d2.keys()]
        d3 = {}
        for i in repeat:
            d3[i] = min(d1[i], d2[i])
        return (d3)
    #优先分到3号位
    gategravity={'3':0.4,'5':0.2,'7':0.2,'L':0.2}
    print('开始求解###################################################')
    prob = pulp.LpProblem('selection', pulp.LpMaximize)
    vars = {}
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            vars[(i, k)] = pulp.LpVariable('%d_%s' % (i, k), lowBound=0, cat='Integer')
    prob += sum(vars[(i, k)] * int(gatelist[k].bridge) * gategravity[gatelist[k].gateno[0]] for i, k in vars.keys())
    # 添加各项约束
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            if union(Q, Z)[i, k] == 0:
                prob += vars[(i, k)] == 0
    ##约束不放松，每个航班当且仅当分配至一个机位
    for i in range(len(flightlist)):
        prob += sum(vars[(i, k)] for k in range(len(gatelist))) == 1
    for k in range(len(gatelist)):
        for i in range(len(flightlist)):
            for j in range(len(flightlist)):
                if T[i, j] == 1:
                    prob += vars[(i, k)] + vars[(j, k)] <= 1
    for i in assigned_apron_flights:
        for k in apron:
            if flightlist[i].pro_gate == gatelist[k].gateno:
                for kk in apron:
                    if kk != k:
                        prob += vars[(i, kk)] == 0

    # 求解问题写入test_1.py文件中
    prob.writeLP('test_1.lp')

    # 求解
    print('开始时间：', time.asctime(time.localtime(time.time())))
    prob.solve()
    print('结束时间：', time.asctime(time.localtime(time.time())))
    # 打印结果
    print('optimize_status: %s' % pulp.LpStatus[prob.status])
    print('var_list:')
    for i in prob.variables():
        # print(i,type(i))
        if i.varValue != 0:
            print('    %s = %s' % (i.name, i.varValue))
    ##定义已分配航班集合
    assigned_flightlist=[]
    for i in prob.variables():
        if i.varValue != 0:
            result=i.name.split('_')
            flightlist[int(result[0])].gate = gatelist[int(result[1])].gateno
            assigned_flightlist.append(i)
            #print(flightlist[int(result[0])].aflightno,flightlist[int(result[0])].destination, flightlist[int(result[0])].atime, flightlist[int(result[0])].dtime,
            #     flightlist[int(result[0])].ParkingGate)

    print('total_value: %d' % pulp.value(prob.objective))
    ##若可拖曳航班在此次分配中未分配机位，则将其gate属性设置为0
    for i in assigned_apron_flights:
        if i not in assigned_flightlist:
            flightlist[i].gate='0'
##############################################################################################################################
##对所有航班尽量往近机位分配：（注意国际国内，机型的匹配）
list_flt=[(external_flightlist_F,internal_flightlist_F),(external_flightlist_E,internal_flightlist_E),(external_flightlist_D,internal_flightlist_D),(external_flightlist_C,internal_flightlist_C)]
list_gt=[(external_near_gatelist_F,internal_near_gatelist_F),(external_near_gatelist_E,internal_near_gatelist_E),(external_near_gatelist_D,internal_near_gatelist_D),(external_near_gatelist_C,internal_near_gatelist_C)]

for i in range(len(list_flt)):
    for index in range(2):
        ##若对应航班集合非空
        for f in (list_flt[i][index]):
            print(f.flightid, f.aflightno,f.dflightno, f.flightnum, f.atime, f.dtime, f.paras, f.mdl, f.apassenger, f.dpassenger, f.nation, f.arrive,f.departure, f.pro_gate, f.gate)

        if len(list_flt[i][index])>0:
            ##取得其可分配的机位集合（如internal_flightlist_E往internal_near_gatelist_F+internal_near_gatelist_E分配）
            gt_sum=[]
            for ii in range(i+1):
                gt_sum += list_gt[ii][index]
            ##利用函数进行分配
            if len(gt_sum)>0:
                gate_assignment_model(list_flt[i][index], gt_sum)
            # 更新每个gate的flightset属性
            for jj in range(i + 1):
                ##对于机位集合中的每一个机位index_gt
                for index_gt in range(len(list_gt[jj][index])):
                    ##对于航班集合中的每一个航班index_flt
                    for index_flt in range(len(list_flt[i][index])):
                        list_gt[jj][index][index_gt].getflight(list_flt[i][index][index_flt])
            ##更新机位空闲时间
            for kk in gt_sum:
                kk.findresttime()
print('近机位航班分配完毕')



##对剩余航班进行分配，分配至远机位中
list_apron=[(external_apron_gatelist_F,internal_apron_gatelist_F),(external_apron_gatelist_E,internal_apron_gatelist_E),(external_apron_gatelist_D,internal_apron_gatelist_D),(external_apron_gatelist_C,internal_apron_gatelist_C)]
for i in range(len(list_flt)):#0~3
    for index in range(2):  #0、1
        noassign_flt=[]
        for kkk in range(len(list_flt[i][index])): #循环所有航班
            if list_flt[i][index][kkk].gate=='0':
                #print (list_flt[i][index][kkk].flightid,list_flt[i][index][kkk].aflightno)
                noassign_flt.append(list_flt[i][index][kkk])


        print (len(noassign_flt),i,index,'ffffff')
        for f in noassign_flt:
            print(f.flightid, f.aflightno,f.dflightno, f.flightnum, f.atime, f.dtime, f.paras, f.mdl, f.apassenger, f.dpassenger, f.nation, f.arrive,f.departure, f.pro_gate, f.gate)


        if len(noassign_flt) > 0:
            gt_sum = []
            for ii in range(i+1):
                gt_sum += list_apron[ii][index]

            print (len(gt_sum),i,index,'gggggg')
            for g in gt_sum:
                print(g.gateno,g.starttime,g.endtime,g.nation,g.mdl)


            if len(gt_sum)>0:
                gate_assignment_model_strict(noassign_flt,gt_sum)
            else:
                print ('没有对应机位，未分配')


            print('分配完毕')
            # 设置每个gate的flightset属性
            for jj in range(i + 1):
                for index_gt in range(len(list_apron[jj][index])):
                    for index_flt in range(len(noassign_flt)):
                        list_apron[jj][index][index_gt].getflight(noassign_flt[index_flt])
            for kk in gt_sum:
                kk.findresttime()

allgate=[]
for i in range(len(list_gt)):
    for j in range(2):
        allgate+=list_gt[i][j]
for i in range(len(list_apron)):
    for j in range(2):
        allgate+=list_apron[i][j]
# print(len(allgate))
# for i in allgate:
#     ff=i.flightset
#     for j in ff:
#         print(i.gateno,j.aflightno,j.atime,j.dtime,j.mdl)

allflight=[]
for i in range(len(list_flt)):
    for j in range(2):
        allflight+=list_flt[i][j]

assign_result={}
bridgeflight=0
finalresult=human_assign_list+allflight
for i in finalresult:
    flightid = i.flightid
    aflightno = i.aflightno
    dflightno = i.dflightno
    flightnum=i.flightnum
    atime = i.atime
    dtime = i.dtime
    paras = i.paras
    mdl = i.mdl
    nation = i.nation
    apassenger = i.apassenger
    dpassenger = i.dpassenger
    arrive = i.arrive
    departure = i.departure
    gate = i.gate
    pro_gate = i.pro_gate
    result={}
    result['flightid'] = flightid
    result['aflightno'] = aflightno
    result['dflightno'] = dflightno
    result['flightnum']=flightnum
    result['atime'] = atime
    result['dtime'] = dtime
    result['paras'] = paras
    result['gate'] = gate
    result['nation'] = nation
    result['mdl'] = mdl
    result['apassenger'] = apassenger
    result['dpassenger'] = dpassenger
    result['arrive'] = arrive
    result['departure'] = departure
    result['pro_gate'] = pro_gate
    assign_result[flightid] = result

for i in finalresult:
    flightid = i.flightid
    aflightno = i.aflightno
    dflightno = i.dflightno
    flightnum=i.flightnum
    atime = i.atime
    dtime = i.dtime
    paras = i.paras
    mdl = i.mdl
    nation = i.nation
    apassenger = i.apassenger
    dpassenger = i.dpassenger
    arrive = i.arrive
    departure = i.departure
    pro_gate = i.pro_gate
    gate = i.gate
    # if gate in remotegate:
    if gate[0]=='1':
        bridgeflight+=1
    print(flightid,aflightno,dflightno,flightnum,atime,dtime,paras,mdl,apassenger,dpassenger,nation,arrive,departure,pro_gate,gate)

print(len(assign_result))
print (bridge_gatenum)
print(bridgeflight)

print(assign_result)
content=str(assign_result)
f = open("0603ad result.txt",'a')
f.write(content)
f.close()

time2=time.asctime(time.localtime(time.time()))
print('程序开始时间：',time1)
print('程序结束时间：',time2)


