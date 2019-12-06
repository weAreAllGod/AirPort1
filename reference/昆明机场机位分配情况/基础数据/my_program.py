# -*- coding: cp936 -*-
# -*- coding:utf-8 -*-
##按空间分割，先对近机位（分成国内，国际两种机位分别进行分配）分配，更新机位空闲时间，再分配远机位
#在建立航班和机位list时     要分为国际航班的list,国内航班list     要分为国内机位（近机位list,远机位list）以及国际机位（近机位list,远机位list）
##下一步再按照机型分类
import time
time1=time.asctime(time.localtime(time.time()))
#目前手工输入分配日期，应该写在发送data的文件开头
assigntime='2018/06/03 00:00'

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

#标准化时间
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

###3.初始化航班和机位数据，得到jstr_flight航班列表
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
    if timed(jstr_flight[i]['atime'])<timed(assigntime) and timed(jstr_flight[i]['dtime'])>=timed(assigntime) :
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

##修改gate属性值
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
        # 修改是否有廊桥，有2无1
    if jstr_gate[i]['bridge'] == '1':
        jstr_gate[i]['bridge'] = '2'
    else:
        jstr_gate[i]['bridge'] = '1'

#数据导入与修改完毕，开始切割数据
###########################################################################
##拆分航班，按国际国内、机型分##############################################
internal_flightlist_C=[]
internal_flightlist_D=[]
internal_flightlist_E=[]
internal_flightlist_F=[]
external_flightlist_C=[]
external_flightlist_D=[]
external_flightlist_E=[]
external_flightlist_F=[]
human_assign_list = [] ##停放在近机位的前一天航班，不能进行拖曳，作为已分配航班不参与机位分配
change_assign_list=[]
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
    elif jstr_flight[i]['paras'] == '1' and (jstr_flight[i]['gate'][0] == '3' or jstr_flight[i]['gate'][0] == '5' or jstr_flight[i]['gate'][0] == '7' or jstr_flight[i]['gate'][0] == 'L'):
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
        change_assign_list.append(flt)
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
#对于国内C型航班数量过多，将其按离港时间排序后分为多组,每组最多25个
try:
    import operator
except ImportError:
    cmpfun = lambda x: x.count  # use a lambda if no operator module
else:
    cmpfun = operator.attrgetter('intdtime')  # use operator since it's faster than lambda
internal_flightlist_C.sort(key=cmpfun)
m=len(internal_flightlist_C)
n=20 #每次分配航班数量：20
internal_flightlist_C=[internal_flightlist_C[i:i + n] for i in range(0, len(internal_flightlist_C), n)]
print('航班与机位状况：')
print('近机位过夜航班数：',len(human_assign_list))
print('远机位过夜可拖曳航班数：',len(change_assign_list))
print('国际C型航班数量：',len(external_flightlist_C))
print('国际D型航班数量：',len(external_flightlist_D))
print('国际E型航班数量：',len(external_flightlist_E))
print('国际F型航班数量：',len(external_flightlist_F))
print('国内C型航班数量：',m,'分隔组数：',len(internal_flightlist_C))
print('国内D型航班数量：',len(internal_flightlist_D))
print('国内E型航班数量：',len(internal_flightlist_E))
print('国内F型航班数量：',len(internal_flightlist_F))
##拆分机位#################################################
##产生gatelist,包含gate对象
external_apron_gatelist_C=[]##国际远机位
external_apron_gatelist_D=[]##国际远机位
external_apron_gatelist_E=[]##国际远机位
external_apron_gatelist_F=[]##国际远机位
external_near_gatelist_C=[]##国际近机位
external_near_gatelist_D=[]##国际近机位
external_near_gatelist_E=[]##国际近机位
external_near_gatelist_F=[]##国际近机位
internal_apron_gatelist_C3=[]##国内远机位3开头
internal_apron_gatelist_C5=[]##国内远机位5开头
internal_apron_gatelist_C7=[]##国内远机位7开头
internal_apron_gatelist_CL=[]##国内远机位L开头
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
    #print(gt.gateno,gt.starttime,gt.endtime,gt.mdl)
    for j in change_assign_list:
        gt.getflight(j)
    gt.findresttime()

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
                if gt.gateno[0]=='3':
                    internal_apron_gatelist_C3.append(gt)
                elif gt.gateno[0]=='5':
                    internal_apron_gatelist_C5.append(gt)
                elif gt.gateno[0]=='7':
                    internal_apron_gatelist_C7.append(gt)
                else:
                    internal_apron_gatelist_CL.append(gt)
            elif gt.mdl == 4:
                internal_apron_gatelist_D.append(gt)
            elif gt.mdl == 5:
                internal_apron_gatelist_E.append(gt)
            else:
                internal_apron_gatelist_F.append(gt)
print('国际远机位C D E F：',len(external_apron_gatelist_C),len(external_apron_gatelist_D),len(external_apron_gatelist_E),len(external_apron_gatelist_F))
print('国际近机位C D E F：',len(external_near_gatelist_C),len(external_near_gatelist_D),len(external_near_gatelist_E),len(external_near_gatelist_F))
print('国内远机位C3 C5 C7 CL D E F：',len(internal_apron_gatelist_C3),len(internal_apron_gatelist_C5),len(internal_apron_gatelist_C7),len(internal_apron_gatelist_CL),len(internal_apron_gatelist_D),len(internal_apron_gatelist_E),len(internal_apron_gatelist_F))
print('国内近机位C D E F：',len(internal_near_gatelist_C),len(internal_near_gatelist_D),len(internal_near_gatelist_E),len(internal_near_gatelist_F))
###########################################
print('###################################')
print('开始进行分配：')
#开始求解#######
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

    #print('Q矩阵处理完毕##################################################')

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

    #print('T矩阵处理完毕###########################################################')
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
    #print('开始求解###################################################')
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
    # ##对于可拖曳航班（已分配航班且分配至远机位），仅能重新分配至近机位或者保持其机位不变
    # for i in assigned_apron_flights:
    #     for k in apron:
    #         if flightlist[i].pro_gate==gatelist[k].gateno:
    #             for kk in apron:
    #                 if kk != k:
    #                     prob += vars[(i, kk)] == 0
    # 求解问题写入test_1.py文件中
    prob.writeLP('test_1.lp')

    # 求解
    print('开始时间：', time.asctime(time.localtime(time.time())))
    prob.solve()
    print('结束时间：', time.asctime(time.localtime(time.time())))
    # 打印结果
    print('optimize_status: %s' % pulp.LpStatus[prob.status])
    if pulp.LpStatus[prob.status] == 'Optimal':
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
                print(flightlist[int(result[0])].flightid, flightlist[int(result[0])].aflightno,flightlist[int(result[0])].dflightno,
                      flightlist[int(result[0])].flightnum, flightlist[int(result[0])].atime, flightlist[int(result[0])].dtime, flightlist[int(result[0])].paras,
                      flightlist[int(result[0])].mdl, flightlist[int(result[0])].nation, flightlist[int(result[0])].arrive, flightlist[int(result[0])].departure,
                      flightlist[int(result[0])].pro_gate, flightlist[int(result[0])].gate)

        print('total_value: %d' % pulp.value(prob.objective))
        # ##若可拖曳航班在此次分配中未分配机位，则将其gate属性设置为0
        # for i in assigned_apron_flights:
        #     if i not in assigned_flightlist:
        #         flightlist[i].gate='0'
    else:
        result1 = {'value': 0}
        return result1
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

    # print('Q矩阵处理完毕############################机型可以停靠1，不可以0.######################')
    # print (Q)

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

    # print('T矩阵处理完毕#############################两航班机位占用时间 冲突1 ，不冲突0.##############################')
    # print (T)
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
    # print('Z矩阵处理完毕##############航班时间属于机位空闲时间段内1，不属于0.##############################')
    # print (Z)


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
    prob += sum(vars[(i, k)] * int(gatelist[k].bridge) for i, k in vars.keys())
    # 添加各项约束
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            if union(Q, Z)[i, k] == 0:
                prob += vars[(i, k)] == 0
    ##约束不放松，每个航班当且仅当分配至一个机位
    for i in range(len(flightlist)):
        prob += sum(vars[(i, k)] for k in range(len(gatelist))) <= 1
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
            print(flightlist[int(result[0])].flightid, flightlist[int(result[0])].aflightno,
                  flightlist[int(result[0])].dflightno,
                  flightlist[int(result[0])].flightnum, flightlist[int(result[0])].atime,
                  flightlist[int(result[0])].dtime, flightlist[int(result[0])].paras,
                  flightlist[int(result[0])].mdl, flightlist[int(result[0])].nation, flightlist[int(result[0])].arrive,
                  flightlist[int(result[0])].departure,
                  flightlist[int(result[0])].pro_gate, flightlist[int(result[0])].gate)
    print('total_value: %d' % pulp.value(prob.objective))
    ##若可拖曳航班在此次分配中未分配机位，则将其gate属性设置为0
    for i in assigned_apron_flights:
        if i not in assigned_flightlist:
            flightlist[i].gate='0'
print('1、开始分配国际C型航班：')
flightlist_1=external_flightlist_C
gatelist_1=external_near_gatelist_C+external_near_gatelist_D
# print('待分配国际C型航班：')
# for f in flightlist_1:
#     print(f.flightid, f.aflightno,f.dflightno, f.flightnum, f.atime, f.dtime, f.paras, f.mdl, f.apassenger, f.dpassenger, f.nation, f.arrive,f.departure, f.pro_gate, f.gate)
gate_assignment_model(flightlist_1,gatelist_1)
for i in gatelist_1:
    for j in flightlist_1:
        i.getflight(j)
for i in gatelist_1:
    i.findresttime()
# for gt in gatelist_1:
#     print(gt.gateno, gt.starttime, gt.endtime, gt.mdl)

print('2、开始分配国际D型航班：')
flightlist_1=external_flightlist_D
gatelist_1=external_near_gatelist_D+external_near_gatelist_E
if len(flightlist_1)>0:
    gate_assignment_model(flightlist_1,gatelist_1)
    for i in gatelist_1:
        for j in flightlist_1:
            i.getflight(j)
    for i in gatelist_1:
        i.findresttime()

print('3、开始分配国内E型航班：')
flightlist_1=internal_flightlist_E
gatelist_1=internal_near_gatelist_E+internal_near_gatelist_F
gate_assignment_model(flightlist_1,gatelist_1)
for i in gatelist_1:
    for j in flightlist_1:
        i.getflight(j)
for i in gatelist_1:
    i.findresttime()

print('4、开始分配国内C型航班至近机位：')
noassign_list=[]
for k in range(len(internal_flightlist_C)):
    flightlist_1=internal_flightlist_C[k]
    #print(len(flightlist_4))
    gatelist_1=internal_near_gatelist_C+internal_near_gatelist_D+internal_near_gatelist_E+internal_near_gatelist_F
    #print(len(gatelist_4))
    print(len(flightlist_1),len(gatelist_1))
    gate_assignment_model(flightlist_1,gatelist_1)
    for i in gatelist_1:
        for j in flightlist_1:
            i.getflight(j)
    for i in gatelist_1:
        i.findresttime()
    for i in flightlist_1:
        if i.gate=='0':
            noassign_list.append(i)

print('5、开始分配剩余航班至远机位,个数为：',len(noassign_list))
#先分C3
gate_assignment_model_strict(noassign_list,internal_apron_gatelist_C3)
#再分C5
noassign_afterC3=[]
for i in noassign_list:
    if i.gate=='0':
        noassign_afterC3.append(i)
gate_assignment_model_strict(noassign_afterC3,internal_apron_gatelist_C5)

