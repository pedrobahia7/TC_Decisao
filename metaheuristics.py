import time
import random
from restrictions import capacidade_excedida

class GVNS:
    def __init__(self, n, m, m_recursos_necessarios, v_capacidade_max, neighbour_structs):
        self.neighbour_structs = neighbour_structs
        self.n = n
        self.m = m
        self.m_recursos_necessarios = m_recursos_necessarios 
        self.v_capacidade_max = v_capacidade_max

    def __best_neighbour(self, x, k, funct):
        all_n = k(x)
        min = funct(all_n[0])
        for n in all_n[1:]:
            n_eval = funct(n)
            if n_eval < min: #minimizacao
                min = n_eval
                best_neighbour = n

        return best_neighbour

    def __best_improvement(self, x, k, funct):
        while True:
            _x = x.copy()
            x = self.__best_neighbour(x, k, funct)
            if capacidade_excedida(self.n, self.m, x, self.m_recursos_necessarios, self.v_capacidade_max): 
                if funct(x) >= funct(_x):
                    return(x)
            else:
                x = _x

    def shake(self, x, k):
        row1, row2 = random.sample(range(5), 2)
        col1, col2 = random.sample(range(50), 2)

        if k == 0:
            new_solution = x.copy()
            new_solution.iloc[row1], new_solution.iloc[row2] = x.iloc[row2], x.iloc[row1]
        if k == 1:
            new_solution = x.copy()
            x_one_idx = x.loc[:,col1].where(x.loc[:,col1]==1).idxmax()
            if new_solution.loc[row1,col1] == 0:
                new_solution.loc[row1,col1] = 1
                new_solution.loc[x_one_idx,col1] = 0
            else:
                new_solution.loc[row2,col1] = 1
                new_solution.loc[x_one_idx,col1] = 0
                
        if k == 2:
            new_solution = x.copy()
            new_solution[col1], new_solution[col2] = x[col2], x[col1]

        return new_solution

    def vnd(self, x, k_max, objective_function):
        k = 0
        while k <= k_max:
            n_struct = self.neighbour_structs[k]
            _x = self.__best_improvement(x, n_struct, objective_function)
            if objective_function(x) < objective_function(_x):
                x = _x.copy()
                k = 0 #reinicializa
            else:
                k = k + 1 #muda estrutura
        return x
    
    def gvns(self, x, l_max, k_max, t_max, objective_function):
        timeout = time.time() + t_max
        k = 0
        while k <= k_max:
            if time.time() > timeout:
                break

            n_struct = self.neighbour_structs[k]
            x_ = self.shake(x, k)
            x__ = self.vnd(x_, l_max, objective_function)

            if objective_function(x) < objective_function(x__):
                x = x__.copy()
                k = 0 #reinicializa
            else:
                k = k + 1 #muda estrutura
        return x
