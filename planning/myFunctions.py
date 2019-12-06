import numpy as np
from scipy.optimize import linprog
import math
import queue
import copy
# c=np.array([1,2,3])
# A_ub = np.array([[-2,1,1],[3,-1,-2]])
# b_ub = np.array([9,-4])
# A_eq = np.array([[3,-2,-3]])
# b_eq = np.array([-6])
# method="interior-point"内点法，revised_simplex修正单纯形法，
# r = linprog(c,A_ub,b_ub,A_eq,b_eq,bounds=((None,0),(0,None),(None,None)),method="simplex")
class solver:
    def solvePro(self,parasList):
        # [cc, Aub, bub, Aeq, beq]
        c=np.array(parasList[0])

        if parasList[1]==None:
            A_b=None
            b_b=None
        else:
            A_b = np.array(parasList[1])
            b_b = np.array(parasList[2])

        if parasList[3][0]==[0 for i in range(len(parasList[3][0]))]:
            A_e=None
            b_e=None
        else:
            A_e = np.array(parasList[3])
            b_e = np.array(parasList[4])
        r = linprog(c, A_ub=A_b, b_ub=b_b,A_eq=A_e, b_eq=b_e, bounds=tuple(parasList[5][0]), method="simplex")
        return r
    # 分支定界
    def branchDelimitation(self,thisProB):
        resultsList=[]
        problemQue=queue.Queue()
        problemQue.put(thisProB)
        while problemQue.empty()!=True:
            thisProB=problemQue.get()
            result =self.solvePro(thisProB)
            # 首先确保有可行解
            if result["success"]==False:
                continue
            judge=True
            for xIndex,x in enumerate(result["x"]):
                if math.floor(x)!=x:
                    judge=False
                    lastLimitation1=copy.deepcopy(thisProB[-1])
                    lastLimitation2=copy.deepcopy(thisProB[-1])
                    lastLimitation1[0][xIndex]=tuple([lastLimitation1[0][xIndex][0],math.floor(x)])
                    lastLimitation2[0][xIndex]=tuple([math.floor(x)+1,lastLimitation2[0][xIndex][1]])
                    problemQue.put(thisProB[:-1]+[lastLimitation1])
                    problemQue.put(thisProB[:-1]+[lastLimitation2])
                    break
            if judge:
                print(result["fun"])
                resultsList.append([result["x"], result["fun"]])
        return resultsList

# thisProB=[[-1, -5], [[-1, 1], [5, 6]], [2, 30], [[0, 0]], [0], [[(0, 4), (0, None)]]]
# thisProB=[[5,-2,3,-6],  None,None,[[1,2,3,4],[2,1,1,2]],[7,3],[[(0, None),(0, None),(0, None),(0, None)]]]
# mySolver=solver()
# allResults=mySolver.branchDelimitation(thisProB)