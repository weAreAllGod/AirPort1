import cplex
from cplex.exceptions import CplexError
from cplex._internal import ProblemType
from cplex._internal import _constants

def cplexSoverMain(v_c, v_matrix,v_b,vType):
    try:
        my_prob = cplex.Cplex()
        my_obj = v_c
        my_prob.set_problem_type(my_prob.problem_type.LP)
        # my_obj = [len(possible) for possible in possibles]
        my_ub = [cplex.infinity for i in range(v_matrix.shape[1])]
        my_lb = [0 for i in range(v_matrix.shape[1])]

        my_ctype = ""
        for i in range(v_matrix.shape[1]):
            my_ctype += vType
        #
        my_colnames = ["y" + str(i) for i in range(v_matrix.shape[1])]
        # names = my_colnames
        # my_colnames = ["y1", "y2", "y3", "y4"]

        my_prob.variables.add(obj=my_obj, lb=my_lb, ub=my_ub,types = my_ctype,
                              names=my_colnames)
        # types = my_ctype,

        my_prob.objective.set_sense(my_prob.objective.sense.maximize)
        rows = []
        for i in range(v_matrix.shape[0]):

            thisLinstraint = [my_colnames,list(v_matrix[i,:])]
            rows.append(thisLinstraint)
        my_rhs = list(v_b)

        my_rownames = ["r" + str(i) for i in range(v_matrix.shape[0])]
        my_sense = ""
        for i in range(v_matrix.shape[0]):
            my_sense += 'L'
        my_prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
                                       rhs=my_rhs, names=my_rownames)
        print("求解开始")
        my_prob.solve()
    except CplexError as exc:
        print(exc)
    return my_prob
def cplexSoverDual(v_c, v_matrix,v_b,vType):
    try:
        my_prob_dual = cplex.Cplex()
        my_prob_dual.set_problem_type( my_prob_dual.problem_type.LP)
        my_obj = v_c

        # my_obj = [len(possible) for possible in possibles]

        my_ub = [cplex.infinity for i in range(v_matrix.shape[1])]
        my_lb = [0 for i in range(v_matrix.shape[1])]

        my_ctype = ""
        for i in range(v_matrix.shape[1]):
            my_ctype += vType
        my_colnames = ["y" + str(i) for i in range(v_matrix.shape[1])]

        my_prob_dual.variables.add(obj=my_obj, lb=my_lb, ub=my_ub,
                              names=my_colnames)
        # types = my_ctype,

        my_prob_dual.objective.set_sense( my_prob_dual.objective.sense.minimize)
        rows = []
        for i in range(v_matrix.shape[0]):
            thisLinstraint = [my_colnames, list(v_matrix[i,:])]
            rows.append(thisLinstraint)
        my_rhs = list(v_b)
        my_rownames = ["r" + str(i) for i in range(v_matrix.shape[0])]
        my_sense = ""
        for i in range(len(rows)):
            my_sense += 'G'
        my_prob_dual.linear_constraints.add(lin_expr=rows, senses=my_sense,
                                       rhs=my_rhs, names=my_rownames)

        my_prob_dual.solve()
        #
        return my_prob_dual
    except CplexError as exc:
        print(exc)



def cplexSoverSub(v_c, v_matrix,v_b,vType):
    try:
        my_prob_sub = cplex.Cplex()

        my_obj = v_c

        my_prob_sub.set_problem_type(my_prob_sub.problem_type.MILP)

        # my_obj = [len(possible) for possible in possibles]

        my_ub = [1 for i in range(v_matrix.shape[1])]
        my_lb = [0 for i in range(v_matrix.shape[1])]

        my_ctype = ""
        for i in range(v_matrix.shape[1]):
            my_ctype += vType
        #
        my_colnames = ["y" + str(i) for i in range(v_matrix.shape[1])]
        # names = my_colnames
        # my_colnames = ["y1", "y2", "y3", "y4"]

        my_prob_sub.variables.add(obj=my_obj, lb=my_lb, ub=my_ub,
                              names=my_colnames,types = my_ctype)
        # types = my_ctype,

        my_prob_sub.objective.set_sense(my_prob_sub.objective.sense.maximize)
        rows = []
        for i in range(v_matrix.shape[0]):
            for j,value in enumerate(v_matrix[i,:]):
                if value==1:
                    thisLinstraint = [["y%s"%(i),"y%s"%(j)], [1,1]]
                    rows.append(thisLinstraint)
        my_rhs = list([1 for i in range(len(rows))])

        my_rownames = ["r" + str(i) for i in range(len(rows))]
        my_sense = ""
        for i in range(len(rows)):
            my_sense += 'L'



        my_prob_sub.linear_constraints.add(lin_expr=rows, senses=my_sense,
                                       rhs=my_rhs, names=my_rownames)
        print("求解开始")
        my_prob_sub.write("2.lp")
        my_prob_sub.solve()
        #
        return my_prob_sub
    except CplexError as exc:
        print(exc)

def cplexForSecondPro(parasForSecondPro,allBounds,result):
    try:
        my_prob = cplex.Cplex()
        my_colnames=[]
        for line in range(len(parasForSecondPro)):
            for column in range(len(parasForSecondPro)):
                if parasForSecondPro[line][column]==1:
                    my_colnames.append("y%s,%s"%(line,column))

        my_ub = [1 for i in range(len(my_colnames))]
        my_lb = [0 for i in range(len(my_colnames))]

        my_ctype = ""
        for i in range(len(my_colnames)):
            my_ctype += "I"
        #
        my_obj = [len(result[int(thisPara.split(",")[0][1:])]) for thisPara in my_colnames]
        # names = my_colnames
        # my_colnames = ["y1", "y2", "y3", "y4"]

        my_prob.variables.add(obj=my_obj, lb=my_lb, ub=my_ub,types = my_ctype,
                              names=my_colnames)
        # types = my_ctype,

        my_prob.objective.set_sense(my_prob.objective.sense.maximize)
        # 首先，行约束
        rows = []
        my_rhs =[]
        for i in range(len(parasForSecondPro)):
            thisLinstraint = [["y%s,%s"%(i,j) for j,value in enumerate(parasForSecondPro[i]) if value==1 ],[1]*len([value1 for value1 in parasForSecondPro[i] if value1==1])]
            rows.append(thisLinstraint)
            my_rhs.append(1)
        # 然后是列约束
        for j in range(len(parasForSecondPro)):
            thisColumn=[item[j] for item in parasForSecondPro]
            thisLinstraint=[["y%s,%s"%(index,j) for index,value in enumerate(thisColumn) if value==1],[1]*len([value1 for value1 in thisColumn if value1==1 ])]
            rows.append(thisLinstraint)
            my_rhs.append(1)
        #然后是位置冲突
        for bound in allBounds:
            thisLinstraint=[[],[]]
            # thisLinstraint =[["y%s,%s"%(item[0],item[1]) for item in bound],[1]%len(bound)]
            for item in bound:
                if item==[61,0]:
                    print("here")
                thisLinstraint[0].append("y%s,%s"%(tuple(item)))
                thisLinstraint[1].append(1)
            rows.append(thisLinstraint)
            my_rhs.append(1)


        my_rownames = ["r" + str(i) for i in range(len(rows))]
        my_sense = ""
        for i in range(len(rows)):
            my_sense += 'L'
        print("到这了")
        my_prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
                                       rhs=my_rhs, names=my_rownames)
        print("求解开始")

        my_prob.solve()
        return my_prob
    except CplexError as exc:
        print(exc)