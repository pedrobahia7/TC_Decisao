import time
import random

class GVNS:
    def __init__(self, m_recursos_necessarios, m_custo_tarefa, v_capacidade_max, neighbour_structs):
        self.neighbour_structs = neighbour_structs
        self.resource = m_recursos_necessarios 
        self.cost = m_custo_tarefa 
        self.max_capacity = v_capacidade_max
        self.evolution_of_f = list()

    def __best_neighbour(self, x, k, funct):
        all_n = k(x)
        min = funct(x, self.cost, self.max_capacity, self.resource)
        best_neighbour = x
        print(min)
        for n in all_n:
            n_eval = funct(n, self.cost, self.max_capacity, self.resource)
            if n_eval < min: #minimizacao
                    min = n_eval
                    best_neighbour = n
            self.evolution_of_f.append(min) #add to value of f
        return best_neighbour

    def __best_improvement(self, x, k, funct):
        while True:
            _x = x.copy()
            x = self.__best_neighbour(x, k, funct)
            if funct(x, self.cost, self.max_capacity, self.resource) >= funct(_x, self.cost, self.max_capacity, self.resource):
                return(x)

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
        while k < k_max:
            n_struct = self.neighbour_structs[k]
            _x = self.__best_improvement(x, n_struct, objective_function)

            if objective_function(x, self.cost, self.max_capacity, self.resource) > objective_function(_x, self.cost, self.max_capacity, self.resource):
                x = _x.copy()
                k = 0 #reinicializa
            else:
                k = k + 1 #muda estrutura
        return x
    
    def gvns(self, x, l_max, k_max, t_max, objective_function):
        timeout = time.time() + t_max
        k = 0
        while k < k_max:
            if time.time() > timeout:
                break

            n_struct = self.neighbour_structs[k]
            x_ = self.shake(x, k)
            x__ = self.vnd(x_, l_max, objective_function)

            if objective_function(x, self.cost, self.max_capacity, self.resource) > objective_function(x__, self.cost, self.max_capacity, self.resource):
                x = x__.copy()
                k = 0 #reinicializa
            else:
                    k = k + 1 #muda estrutura
        return x

    def normalize(self, solution, min_solution, max_solution):
        return (solution - min_solution)/(max_solution - min_solution)

    def soma_ponderada_biobjetivo(self, x, initial_f1, initial_f2, l_max, k_max, t_max, f1, f2, neg_f1, neg_f2):
        x_min_f1 = self.gvns(initial_f1, l_max, k_max, t_max, f1)
        x_max_f1 = self.gvns(initial_f1, l_max, k_max, t_max, neg_f1)
        x_min_f2 = self.gvns(initial_f2, l_max, k_max, t_max, f2)
        x_max_f2 = self.gvns(initial_f2, l_max, k_max, t_max, neg_f2)

        min_f1 = f1(x_min_f1, self.cost, self.max_capacity, self.resource)
        max_f1 = f1(x_max_f1, self.cost, self.max_capacity, self.resource)
        print(f"f1: {min_f1} ---- {max_f1}")
        z1 = min_f1

        min_f2 = f2(x_min_f2, self.cost, self.max_capacity, self.resource)
        max_f2 = f2(x_max_f2, self.cost, self.max_capacity, self.resource)
        print(f"f2: {min_f2} ---- {max_f2}")
        z2 = min_f2

        lambda1 = self.normalize(z1, min_f2, max_f2 ) - self.normalize(z2, min_f2, max_f2 )
        lambda2 = self.normalize(z2, min_f1, max_f1 ) - self.normalize(z1, min_f1, max_f1 )

        print(f"lambdas: {lambda1} ---- {lambda2}")

        Z = lambda _x, cost, capacity, resource : lambda1*f1(_x, cost, capacity, resource) + lambda2*f2(_x, cost, capacity, resource)
        res = self.gvns(x, l_max, k_max, t_max, Z)
        print("\n\n-----------Solutions --------\n\n")
        print("fc(solution_C): ", f1(res, self.cost, self.max_capacity, self.resource))
        print("fe(solution_E): ", f2(res, self.cost, self.max_capacity, self.resource))

