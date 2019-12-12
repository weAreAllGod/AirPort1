import cplex
from cplex.exceptions import CplexError
my_pro=cplex.Cplex()
my_pro.read("2.lp")
my_pro.solve()