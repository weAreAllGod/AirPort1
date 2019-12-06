# -*- coding: cp936 -*-
# -*- coding:utf-8 -*-
##���ռ�ָ�ȶԽ���λ���ֳɹ��ڣ��������ֻ�λ�ֱ���з��䣩���䣬���»�λ����ʱ�䣬�ٷ���Զ��λ
#�ڽ�������ͻ�λlistʱ     Ҫ��Ϊ���ʺ����list,���ں���list     Ҫ��Ϊ���ڻ�λ������λlist,Զ��λlist���Լ����ʻ�λ������λlist,Զ��λlist��
##��һ���ٰ��ջ��ͷ���
import time
time1=time.asctime(time.localtime(time.time()))
#Ŀǰ�ֹ�����������ڣ�Ӧ��д�ڷ���data���ļ���ͷ
assigntime='2018/06/03 00:00'

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

#��׼��ʱ��
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

###3.��ʼ������ͻ�λ���ݣ��õ�jstr_flight�����б�
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

##�޸�gate����ֵ
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
        # �޸��Ƿ������ţ���2��1
    if jstr_gate[i]['bridge'] == '1':
        jstr_gate[i]['bridge'] = '2'
    else:
        jstr_gate[i]['bridge'] = '1'

#���ݵ������޸���ϣ���ʼ�и�����
###########################################################################
##��ֺ��࣬�����ʹ��ڡ����ͷ�##############################################
internal_flightlist_C=[]
internal_flightlist_D=[]
internal_flightlist_E=[]
internal_flightlist_F=[]
external_flightlist_C=[]
external_flightlist_D=[]
external_flightlist_E=[]
external_flightlist_F=[]
human_assign_list = [] ##ͣ���ڽ���λ��ǰһ�캽�࣬���ܽ�����ҷ����Ϊ�ѷ��亽�಻�����λ����
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
#���ڹ���C�ͺ����������࣬���䰴���ʱ��������Ϊ����,ÿ�����25��
try:
    import operator
except ImportError:
    cmpfun = lambda x: x.count  # use a lambda if no operator module
else:
    cmpfun = operator.attrgetter('intdtime')  # use operator since it's faster than lambda
internal_flightlist_C.sort(key=cmpfun)
m=len(internal_flightlist_C)
n=20 #ÿ�η��亽��������20
internal_flightlist_C=[internal_flightlist_C[i:i + n] for i in range(0, len(internal_flightlist_C), n)]
print('�������λ״����')
print('����λ��ҹ��������',len(human_assign_list))
print('Զ��λ��ҹ����ҷ��������',len(change_assign_list))
print('����C�ͺ���������',len(external_flightlist_C))
print('����D�ͺ���������',len(external_flightlist_D))
print('����E�ͺ���������',len(external_flightlist_E))
print('����F�ͺ���������',len(external_flightlist_F))
print('����C�ͺ���������',m,'�ָ�������',len(internal_flightlist_C))
print('����D�ͺ���������',len(internal_flightlist_D))
print('����E�ͺ���������',len(internal_flightlist_E))
print('����F�ͺ���������',len(internal_flightlist_F))
##��ֻ�λ#################################################
##����gatelist,����gate����
external_apron_gatelist_C=[]##����Զ��λ
external_apron_gatelist_D=[]##����Զ��λ
external_apron_gatelist_E=[]##����Զ��λ
external_apron_gatelist_F=[]##����Զ��λ
external_near_gatelist_C=[]##���ʽ���λ
external_near_gatelist_D=[]##���ʽ���λ
external_near_gatelist_E=[]##���ʽ���λ
external_near_gatelist_F=[]##���ʽ���λ
internal_apron_gatelist_C3=[]##����Զ��λ3��ͷ
internal_apron_gatelist_C5=[]##����Զ��λ5��ͷ
internal_apron_gatelist_C7=[]##����Զ��λ7��ͷ
internal_apron_gatelist_CL=[]##����Զ��λL��ͷ
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
    #print(gt.gateno,gt.starttime,gt.endtime,gt.mdl)
    for j in change_assign_list:
        gt.getflight(j)
    gt.findresttime()

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
print('����Զ��λC D E F��',len(external_apron_gatelist_C),len(external_apron_gatelist_D),len(external_apron_gatelist_E),len(external_apron_gatelist_F))
print('���ʽ���λC D E F��',len(external_near_gatelist_C),len(external_near_gatelist_D),len(external_near_gatelist_E),len(external_near_gatelist_F))
print('����Զ��λC3 C5 C7 CL D E F��',len(internal_apron_gatelist_C3),len(internal_apron_gatelist_C5),len(internal_apron_gatelist_C7),len(internal_apron_gatelist_CL),len(internal_apron_gatelist_D),len(internal_apron_gatelist_E),len(internal_apron_gatelist_F))
print('���ڽ���λC D E F��',len(internal_near_gatelist_C),len(internal_near_gatelist_D),len(internal_near_gatelist_E),len(internal_near_gatelist_F))
###########################################
print('###################################')
print('��ʼ���з��䣺')
#��ʼ���#######
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

    #print('Q���������##################################################')

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

    #print('T���������###########################################################')
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
    #print('��ʼ���###################################################')
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
    # ##���ڿ���ҷ���ࣨ�ѷ��亽���ҷ�����Զ��λ�����������·���������λ���߱������λ����
    # for i in assigned_apron_flights:
    #     for k in apron:
    #         if flightlist[i].pro_gate==gatelist[k].gateno:
    #             for kk in apron:
    #                 if kk != k:
    #                     prob += vars[(i, kk)] == 0
    # �������д��test_1.py�ļ���
    prob.writeLP('test_1.lp')

    # ���
    print('��ʼʱ�䣺', time.asctime(time.localtime(time.time())))
    prob.solve()
    print('����ʱ�䣺', time.asctime(time.localtime(time.time())))
    # ��ӡ���
    print('optimize_status: %s' % pulp.LpStatus[prob.status])
    if pulp.LpStatus[prob.status] == 'Optimal':
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
                print(flightlist[int(result[0])].flightid, flightlist[int(result[0])].aflightno,flightlist[int(result[0])].dflightno,
                      flightlist[int(result[0])].flightnum, flightlist[int(result[0])].atime, flightlist[int(result[0])].dtime, flightlist[int(result[0])].paras,
                      flightlist[int(result[0])].mdl, flightlist[int(result[0])].nation, flightlist[int(result[0])].arrive, flightlist[int(result[0])].departure,
                      flightlist[int(result[0])].pro_gate, flightlist[int(result[0])].gate)

        print('total_value: %d' % pulp.value(prob.objective))
        # ##������ҷ�����ڴ˴η�����δ�����λ������gate��������Ϊ0
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

    # ����Q�����жϻ�λ����ƥ���Լ����ʹ�������ƥ�䣩������ΪmdlΪ���ͣ�peopleΪ���ʹ�������,�Ҿ�Ϊ�ַ�������
    Q = {}
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            if (int(gatelist[k].mdl) - int(flightlist[i].mdl)) >= 0 and int(flightlist[i].nation) == int(
                    gatelist[k].nation):
                Q[(i, k)] = 1
            else:
                Q[(i, k)] = 0

    # print('Q���������############################���Ϳ���ͣ��1��������0.######################')
    # print (Q)

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

    # print('T���������#############################�������λռ��ʱ�� ��ͻ1 ������ͻ0.##############################')
    # print (T)
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
    # print('Z���������##############����ʱ�����ڻ�λ����ʱ�����1��������0.##############################')
    # print (Z)


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
    prob += sum(vars[(i, k)] * int(gatelist[k].bridge) for i, k in vars.keys())
    # ��Ӹ���Լ��
    for i in range(len(flightlist)):
        for k in range(len(gatelist)):
            if union(Q, Z)[i, k] == 0:
                prob += vars[(i, k)] == 0
    ##Լ�������ɣ�ÿ�����൱�ҽ���������һ����λ
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
            print(flightlist[int(result[0])].flightid, flightlist[int(result[0])].aflightno,
                  flightlist[int(result[0])].dflightno,
                  flightlist[int(result[0])].flightnum, flightlist[int(result[0])].atime,
                  flightlist[int(result[0])].dtime, flightlist[int(result[0])].paras,
                  flightlist[int(result[0])].mdl, flightlist[int(result[0])].nation, flightlist[int(result[0])].arrive,
                  flightlist[int(result[0])].departure,
                  flightlist[int(result[0])].pro_gate, flightlist[int(result[0])].gate)
    print('total_value: %d' % pulp.value(prob.objective))
    ##������ҷ�����ڴ˴η�����δ�����λ������gate��������Ϊ0
    for i in assigned_apron_flights:
        if i not in assigned_flightlist:
            flightlist[i].gate='0'
print('1����ʼ�������C�ͺ��ࣺ')
flightlist_1=external_flightlist_C
gatelist_1=external_near_gatelist_C+external_near_gatelist_D
# print('���������C�ͺ��ࣺ')
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

print('2����ʼ�������D�ͺ��ࣺ')
flightlist_1=external_flightlist_D
gatelist_1=external_near_gatelist_D+external_near_gatelist_E
if len(flightlist_1)>0:
    gate_assignment_model(flightlist_1,gatelist_1)
    for i in gatelist_1:
        for j in flightlist_1:
            i.getflight(j)
    for i in gatelist_1:
        i.findresttime()

print('3����ʼ�������E�ͺ��ࣺ')
flightlist_1=internal_flightlist_E
gatelist_1=internal_near_gatelist_E+internal_near_gatelist_F
gate_assignment_model(flightlist_1,gatelist_1)
for i in gatelist_1:
    for j in flightlist_1:
        i.getflight(j)
for i in gatelist_1:
    i.findresttime()

print('4����ʼ�������C�ͺ���������λ��')
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

print('5����ʼ����ʣ�ຽ����Զ��λ,����Ϊ��',len(noassign_list))
#�ȷ�C3
gate_assignment_model_strict(noassign_list,internal_apron_gatelist_C3)
#�ٷ�C5
noassign_afterC3=[]
for i in noassign_list:
    if i.gate=='0':
        noassign_afterC3.append(i)
gate_assignment_model_strict(noassign_afterC3,internal_apron_gatelist_C5)

