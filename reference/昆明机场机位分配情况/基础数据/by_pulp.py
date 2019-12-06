# -*- coding: cp936 -*-
# -*- coding:utf-8 -*-
##���ռ�ָ�ȶԽ���λ���ֳɹ��ڣ��������ֻ�λ�ֱ���з��䣩���䣬���»�λ����ʱ�䣬�ٷ���Զ��λ
#�ڽ�������ͻ�λlistʱ     Ҫ��Ϊ���ʺ����list,���ں���list     Ҫ��Ϊ���ڻ�λ������λlist,Զ��λlist���Լ����ʻ�λ������λlist,Զ��λlist��
##��һ���ٰ��ջ��ͷ���
import time
time1=time.asctime(time.localtime(time.time()))
#Ŀǰ�ֹ�����������ڣ�Ӧ��д�ڷ���data���ļ���ͷ
assigntime='2017/06/03 00:00'
# final_starttime='2017/04/10 00:00'
# final_endtime='2017/04/12 00:00'
# ʱ��ת�������������ӣ�
def timed(a):
    timeArray = time.strptime(a, "%Y/%m/%d %H:%M")
    timeStamp = int(time.mktime(timeArray)) / 60
    return timeStamp
# ���Ӹ�����ת���ɱ�׼ʱ�亯��
def datetimed(a):
    timeTuple = time.localtime(a*60)
    timeArray=time.strftime('%Y/%m/%d %H:%M',timeTuple)
    return timeArray

final_starttime=datetimed(timed(assigntime)-1440*2) #��������ǰ48Сʱ
final_endtime=datetimed(timed(assigntime)+1440*2) #�������ں�48Сʱ


# ʱ��ת��Ϊ��׼���ڸ�ʽ
# import time
# def timestandard(a):
#     day_now = time.localtime()
#     fulldate='%s(%d%02d%s)' %(a[0:4],day_now.tm_year, day_now.tm_mon,a[5:7])
#     timeArray = time.strptime(fulldate, "%H%M(%Y%m%d)")
#     timeStandard = time.strftime("%Y/%m/%d %H:%M", timeArray)
#     return timeStandard

#�����·����£�
def timestandard(a):
    day_now = time.localtime()
    fulldate='%s(%d06%s)' %(a[0:4],day_now.tm_year,a[5:7])
    timeArray = time.strptime(fulldate, "%H%M(%Y%m%d)")
    timeStandard = time.strftime("%Y/%m/%d %H:%M", timeArray)
    return timeStandard

##1.����flight��
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

##2.����gate��
class Gate:
    def __init__(self,gateno,mdl,nation,bridge,starttime,endtime):
        self.gateno=gateno
        self.mdl=mdl
        self.nation=nation
        self.bridge=bridge
        self.starttime=starttime
        self.endtime=endtime
        self.flightset=[]
    ##�����෽�����Ѻ�����ӽ����Ӧ�ĺ���ƻ�flightset��
    def getflight(self,flight):
        if flight.gate==self.gateno:
            self.flightset.append(flight)
    ##�����෽����Ѱ�ҿ���ʱ�䣩
    ##�ȶ�flightset�еĺ���������򣬰��պ���ĵ���ʱ����С��������Ȼ�����λ�ÿ���ʱ��
    def findresttime(self):
        flightset=self.flightset
        try:
            import operator
        except ImportError:
            cmpfun = lambda x: x.count  # use a lambda if no operator module
        else:
            cmpfun = operator.attrgetter('intatime')  # use operator since it's faster than lambda
        flightset.sort(key=cmpfun)
        #��ʼ��ʱ��    starttime = [final_starttime]�� endtime = [final_endtime]
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

###3.��ʼ������ͻ�λ����
assignment = open("0603ad-csv.csv", 'r')
next(assignment)  # ������һ�б�ͷ���ӵڶ��п�ʼ������
jstr_flight = []
id=0
for line in assignment:
    line = line.rstrip().split(',')
    if line[0]!='':
        jstr_flight.append({'flightid': str(id), 'aflightno': line[0], 'dflightno': line[1], 'flightnum': line[2], 'atime': line[3],
                   'dtime': line[4], 'paras': line[5], 'mdl': line[6], 'gate': line[7],
                   'nation': line[8], 'apassenger': line[9], 'dpassenger': line[10]})
        id=id+1

# ����λ����csv��д��list �����ݸ�ʽΪ[{item1:xx,item2:xx},{item1:xx,item2:xx}]
gatedata = open("gate-csv.csv", 'r')
next(gatedata)  # ������һ�б�ͷ���ӵڶ��п�ʼ������
jstr_gate = []
for line in gatedata:
    line = line.rstrip().split(',')
    jstr_gate.append({'gateno': line[0], 'mdl': line[1], 'nation': line[2], 'bridge': line[3], 'starttime': line[4]})

#��ȡ���ʺ����ʶ����
f = open("nation.txt","r")
lines = f.readlines()
nation=[]
for line in lines:
    line=line.strip('\n')
    nation.append(line)

bridge_gatenum=0
##����޸ĺ�������ֵ
for i in range(len(jstr_flight)):
    if jstr_flight[i]['gate'][0]=='1':
        bridge_gatenum =bridge_gatenum+1
    ##����ʱ���ʽΪ��׼��ʽ
    jstr_flight[i]['atime']=timestandard(jstr_flight[i]['atime'])
    jstr_flight[i]['dtime'] = timestandard(jstr_flight[i]['dtime'])
    ##��flight�����л������ݸ�Ϊ��ֵ
    if jstr_flight[i]['mdl'][-1]=='C':
        jstr_flight[i]['mdl'] = 3
    elif jstr_flight[i]['mdl'][-1] == 'D':
        jstr_flight[i]['mdl'] = 4
    elif jstr_flight[i]['mdl'][-1] == 'E':
        jstr_flight[i]['mdl'] = 5
    else:
        jstr_flight[i]['mdl'] = 6
     ##flight���� ���paras��arrive��departure��nation����
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


##��gate�����л������ݸ�Ϊ��ֵ
for i in range(len(jstr_gate)):
    if jstr_gate[i]['mdl'] == 'C':
        jstr_gate[i]['mdl'] = 3
    elif jstr_gate[i]['mdl'] == 'D':
        jstr_gate[i]['mdl'] = 4
    elif jstr_gate[i]['mdl'] == 'E':
        jstr_gate[i]['mdl'] = 5
    else:
        jstr_gate[i]['mdl'] = 6
    # �޸����Ĺ��ʹ�������Ϊ0��1
    if jstr_gate[i]['nation']=='����':
        jstr_gate[i]['nation']='1'
    else:
        jstr_gate[i]['nation'] ='0'
        # �޸����Ĺ��ʹ�������Ϊ0��1
    if jstr_gate[i]['bridge'] == '1':
        jstr_gate[i]['bridge'] = '2'
    else:
        jstr_gate[i]['bridge'] = '1'
######################################################################################################################################
##����internal_flightlist���ں��༯�ϣ��Լ�external_flightlist���ʺ��༯�ϣ�����flight����
internal_flightlist_C=[]
internal_flightlist_D=[]
internal_flightlist_E=[]
internal_flightlist_F=[]
external_flightlist_C=[]
external_flightlist_D=[]
external_flightlist_E=[]
external_flightlist_F=[]
##ͣ���ڽ���λ�����ܽ�����ҷ����Ϊ�ѷ��亽�಻�����λ���䣬������ڶɳ�����
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
    ##��Ҫ���з���ĺ���(����û�л�λ�ĺ����Լ����䵽Զ��λ�ĵ��������)
    else:# �ѽ��۵�Զ��λ��δ����
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

# �������л�λ�Ķ��󼯺�
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

# Զ��λ���󼯺�????????????
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
##����gatelist,����gate����
external_apron_gatelist_C=[]##����Զ��λ
external_apron_gatelist_D=[]##����Զ��λ
external_apron_gatelist_E=[]##����Զ��λ
external_apron_gatelist_F=[]##����Զ��λ
external_near_gatelist_C=[]##���ʽ���λ
external_near_gatelist_D=[]##���ʽ���λ
external_near_gatelist_E=[]##���ʽ���λ
external_near_gatelist_F=[]##���ʽ���λ
internal_apron_gatelist_C=[]##����Զ��λ
internal_apron_gatelist_D=[]##����Զ��λ
internal_apron_gatelist_E=[]##����Զ��λ
internal_apron_gatelist_F=[]##����Զ��λ
internal_near_gatelist_C=[]##���ڽ���λ
internal_near_gatelist_D=[]##���ڽ���λ
internal_near_gatelist_E=[]##���ڽ���λ
internal_near_gatelist_F=[]##���ڽ���λ
##���ݻ�λ�Ĺ��ʹ������ԣ��Ƿ�ӵ�����ż������ɻ��ͽ���λ����ֱ���벻ͬ�Ļ�λ������
for i in range(len(jstr_gate)):
    gateno = jstr_gate[i]['gateno']
    mdl = jstr_gate[i]['mdl']
    nation = jstr_gate[i]['nation']
    bridge = jstr_gate[i]['bridge']
    starttime = [final_starttime]
    endtime = [final_endtime]
    gt=Gate(gateno,mdl,nation,bridge,starttime,endtime)
    ##��ÿ����λ���ԣ��������ʼ����ʱ��
    ##�����������ĺ����������λflightset�У�����һ�����³�ʼ��λ����ʱ��
    for j in human_assign_list:
        gt.getflight(j)
    gt.findresttime()
    print(gt.gateno,gt.starttime,gt.endtime,gt.mdl)

    ##����
    if gt.nation == '1':
        ##����������
        if gt.bridge == '2':
            if gt.mdl == 3:
                external_near_gatelist_C.append(gt)
            elif gt.mdl == 4:
                external_near_gatelist_D.append(gt)
            elif gt.mdl == 5:
                external_near_gatelist_E.append(gt)
            else:
                external_near_gatelist_F.append(gt)
        ##����û������
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
        ##����������
        if gt.bridge == '2':
            if gt.mdl == 3:
                internal_near_gatelist_C.append(gt)
            elif gt.mdl == 4:
                internal_near_gatelist_D.append(gt)
            elif gt.mdl == 5:
                internal_near_gatelist_E.append(gt)
            else:
                internal_near_gatelist_F.append(gt)
        ##����û������
        else:
            if gt.mdl == 3:
                internal_apron_gatelist_C.append(gt)
            elif gt.mdl == 4:
                internal_apron_gatelist_D.append(gt)
            elif gt.mdl == 5:
                internal_apron_gatelist_E.append(gt)
            else:
                internal_apron_gatelist_F.append(gt)
                ###��ʼ���з���
##############################################################################################################################
##������⺯��
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

    # ����Q�����жϻ�λ����ƥ���Լ����ʹ�������ƥ�䣩������ΪmdlΪ���ͣ�peopleΪ���ʹ�������,�Ҿ�Ϊ�ַ������� ������ͣ��1��������0.
    Q = {}
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            if (int(gatelist[k].mdl) - int(flightlist[i].mdl)) >= 0 and int(flightlist[i].nation) == int(gatelist[k].nation):
                Q[(i, k)] = 1
            else:
                Q[(i, k)] = 0

    print('Q���������##################################################')

    # ���庯���ж�ʱ���Ƿ��ͻisTimeCollision
    def isTimeCollision(a, b, c, d):
        if (b > c and b <= d) or (d > a and d <= b):
            return 1
        elif (a >= c and a < d) or (c >= a and c < b):
            return 1
        else:
            return 0

    # ��ʼ����T�����ж��������λռ��ʱ���Ƿ��ͻ�����Ҹ���Tb/2�� ��ͻ1 ������ͻ0.
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

    print('T���������###########################################################')
    # ��ʼ����Z����(����ʱ���) ����ʱ�����ڻ�λ����ʱ�����1��������0
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


    # ���캯����������ϲ�����ֵȡС
    def union(d1, d2):
        repeat = [i for i in d1.keys() if i in d2.keys()]
        d3 = {}
        for i in repeat:
            d3[i] = min(d1[i], d2[i])
        return (d3)
    print('��ʼ���###################################################')
    prob = pulp.LpProblem('selection', pulp.LpMaximize)
    vars = {}
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            vars[(i, k)] = pulp.LpVariable('%d_%s' % (i, k), lowBound=0, cat='Integer')
    # # ����Ŀ�꺯������󻯷���������λ�ĺ���������
    # m.setObjective(quicksum(x[i, k] * int(gatelist[k].bridge) for i, k in arcs),
    #                GRB.MAXIMIZE)
    prob += sum(vars[(i, k)] * int(gatelist[k].bridge) for i, k in vars.keys())
    # ��Ӹ���Լ��
    ## ƥ����Լ�������Q��Z����
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            if union(Q, Z)[i, k] == 0:
                prob += vars[(i, k)] == 0
    ##ÿ������������һ����λ��Լ�����ɣ�
    for i in range(len(flightlist)):
        prob += sum(vars[(i, k)] for k in range(len(gatelist))) <= 1
    ##��λռ��ʱ���ͻ�ĺ��಻�ܷ�����ͬһ����λ
    for k in range(len(gatelist)):
        for i in range(len(flightlist)):
            for j in range(len(flightlist)):
                if T[i, j] == 1:
                    prob += vars[(i, k)] + vars[(j, k)] <= 1
    ##���ڿ���ҷ���ࣨ�ѷ��亽���ҷ�����Զ��λ�����������·���������λ���߱������λ����
    for i in assigned_apron_flights:
        for k in apron:
            if flightlist[i].pro_gate==gatelist[k].gateno:
                for kk in apron:
                    if kk != k:
                        prob += vars[(i, kk)] == 0
    # �������д��test_1.py�ļ���
    prob.writeLP('test_1.lp')

    # ���
    print('��ʼʱ�䣺', time.asctime(time.localtime(time.time())))
    prob.solve()
    print('����ʱ�䣺', time.asctime(time.localtime(time.time())))
    # ��ӡ���
    print('optimize_status: %s' % pulp.LpStatus[prob.status])
    print('var_list:')
    for i in prob.variables():
        # print(i,type(i))
        if i.varValue != 0:
            print('    %s = %s' % (i.name, i.varValue))
    ##�����ѷ��亽�༯��
    assigned_flightlist=[]
    for i in prob.variables():
        if i.varValue != 0:
            result=i.name.split('_')
            flightlist[int(result[0])].gate = gatelist[int(result[1])].gateno
            assigned_flightlist.append(i)
            #print(flightlist[int(result[0])].aflightno,flightlist[int(result[0])].destination, flightlist[int(result[0])].atime, flightlist[int(result[0])].dtime,
            #     flightlist[int(result[0])].ParkingGate)

    print('total_value: %d' % pulp.value(prob.objective))
    ##������ҷ�����ڴ˴η�����δ�����λ������gate��������Ϊ0
    for i in assigned_apron_flights:
        if i not in assigned_flightlist:
            flightlist[i].gate='0'
################################################################################################################################
##������⺯��
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

    # ����Q�����жϻ�λ����ƥ���Լ����ʹ�������ƥ�䣩������ΪmdlΪ���ͣ�peopleΪ���ʹ�������,�Ҿ�Ϊ�ַ�������
    Q = {}
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            if (int(gatelist[k].mdl) - int(flightlist[i].mdl)) >= 0 and int(flightlist[i].nation) == int(
                    gatelist[k].nation):
                Q[(i, k)] = 1
            else:
                Q[(i, k)] = 0

    print('Q���������############################���Ϳ���ͣ��1��������0.######################')
    print (Q)

    # ���庯���ж�ʱ���Ƿ��ͻisTimeCollision
    def isTimeCollision(a, b, c, d):
        if (b > c and b <= d) or (d > a and d <= b):
            return 1
        elif (a >= c and a < d) or (c >= a and c < b):
            return 1
        else:
            return 0

    # ��ʼ����T�����ж��������λռ��ʱ���Ƿ��ͻ�����Ҹ���Tb/2��
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

    print('T���������#############################�������λռ��ʱ�� ��ͻ1 ������ͻ0.##############################')
    print (T)
    # ��ʼ����Z����(����ʱ���)
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
    print('Z���������##############����ʱ�����ڻ�λ����ʱ�����1��������0.##############################')
    print (Z)


    # ���캯����������ϲ�����ֵȡС
    def union(d1, d2):
        repeat = [i for i in d1.keys() if i in d2.keys()]
        d3 = {}
        for i in repeat:
            d3[i] = min(d1[i], d2[i])
        return (d3)
    #���ȷֵ�3��λ
    gategravity={'3':0.4,'5':0.2,'7':0.2,'L':0.2}
    print('��ʼ���###################################################')
    prob = pulp.LpProblem('selection', pulp.LpMaximize)
    vars = {}
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            vars[(i, k)] = pulp.LpVariable('%d_%s' % (i, k), lowBound=0, cat='Integer')
    prob += sum(vars[(i, k)] * int(gatelist[k].bridge) * gategravity[gatelist[k].gateno[0]] for i, k in vars.keys())
    # ��Ӹ���Լ��
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            if union(Q, Z)[i, k] == 0:
                prob += vars[(i, k)] == 0
    ##Լ�������ɣ�ÿ�����൱�ҽ���������һ����λ
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

    # �������д��test_1.py�ļ���
    prob.writeLP('test_1.lp')

    # ���
    print('��ʼʱ�䣺', time.asctime(time.localtime(time.time())))
    prob.solve()
    print('����ʱ�䣺', time.asctime(time.localtime(time.time())))
    # ��ӡ���
    print('optimize_status: %s' % pulp.LpStatus[prob.status])
    print('var_list:')
    for i in prob.variables():
        # print(i,type(i))
        if i.varValue != 0:
            print('    %s = %s' % (i.name, i.varValue))
    ##�����ѷ��亽�༯��
    assigned_flightlist=[]
    for i in prob.variables():
        if i.varValue != 0:
            result=i.name.split('_')
            flightlist[int(result[0])].gate = gatelist[int(result[1])].gateno
            assigned_flightlist.append(i)
            #print(flightlist[int(result[0])].aflightno,flightlist[int(result[0])].destination, flightlist[int(result[0])].atime, flightlist[int(result[0])].dtime,
            #     flightlist[int(result[0])].ParkingGate)

    print('total_value: %d' % pulp.value(prob.objective))
    ##������ҷ�����ڴ˴η�����δ�����λ������gate��������Ϊ0
    for i in assigned_apron_flights:
        if i not in assigned_flightlist:
            flightlist[i].gate='0'
##############################################################################################################################
##�����к��ྡ��������λ���䣺��ע����ʹ��ڣ����͵�ƥ�䣩
list_flt=[(external_flightlist_F,internal_flightlist_F),(external_flightlist_E,internal_flightlist_E),(external_flightlist_D,internal_flightlist_D),(external_flightlist_C,internal_flightlist_C)]
list_gt=[(external_near_gatelist_F,internal_near_gatelist_F),(external_near_gatelist_E,internal_near_gatelist_E),(external_near_gatelist_D,internal_near_gatelist_D),(external_near_gatelist_C,internal_near_gatelist_C)]

for i in range(len(list_flt)):
    for index in range(2):
        ##����Ӧ���༯�Ϸǿ�
        for f in (list_flt[i][index]):
            print(f.flightid, f.aflightno,f.dflightno, f.flightnum, f.atime, f.dtime, f.paras, f.mdl, f.apassenger, f.dpassenger, f.nation, f.arrive,f.departure, f.pro_gate, f.gate)

        if len(list_flt[i][index])>0:
            ##ȡ����ɷ���Ļ�λ���ϣ���internal_flightlist_E��internal_near_gatelist_F+internal_near_gatelist_E���䣩
            gt_sum=[]
            for ii in range(i+1):
                gt_sum += list_gt[ii][index]
            ##���ú������з���
            if len(gt_sum)>0:
                gate_assignment_model(list_flt[i][index], gt_sum)
            # ����ÿ��gate��flightset����
            for jj in range(i + 1):
                ##���ڻ�λ�����е�ÿһ����λindex_gt
                for index_gt in range(len(list_gt[jj][index])):
                    ##���ں��༯���е�ÿһ������index_flt
                    for index_flt in range(len(list_flt[i][index])):
                        list_gt[jj][index][index_gt].getflight(list_flt[i][index][index_flt])
            ##���»�λ����ʱ��
            for kk in gt_sum:
                kk.findresttime()
print('����λ����������')



##��ʣ�ຽ����з��䣬������Զ��λ��
list_apron=[(external_apron_gatelist_F,internal_apron_gatelist_F),(external_apron_gatelist_E,internal_apron_gatelist_E),(external_apron_gatelist_D,internal_apron_gatelist_D),(external_apron_gatelist_C,internal_apron_gatelist_C)]
for i in range(len(list_flt)):#0~3
    for index in range(2):  #0��1
        noassign_flt=[]
        for kkk in range(len(list_flt[i][index])): #ѭ�����к���
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
                print ('û�ж�Ӧ��λ��δ����')


            print('�������')
            # ����ÿ��gate��flightset����
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
print('����ʼʱ�䣺',time1)
print('�������ʱ�䣺',time2)


