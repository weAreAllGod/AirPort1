import cplex
import cplex.exceptions
my_test_pro=cplex.Cplex()
my_test_pro.read("test.lp")
my_test_pro.solve()
# my_test_pro.solution.get_values()