import time

class GVNS:
    def __init__(self, neighbour_structs):
        self.neighbour_structs = neighbour_structs

    def __findall_neighbours(self, x, k): #TODO
        pass

    def __best_neighbour(self, x, k, funct):
        all_n = self.__findall_neighbours(x, k)

        min = funct(all_n[0])
        for n in all_n[1:]:
            n_eval = funct(n)
            if n_eval < min: #minimizacao
                min = n_eval
                best_neighbour = n

        return best_neighbour

    def __best_improvement(self, x, k, funct):
        while True:
            _x = x
            x = self.__best_neighbour(x, k, funct)
            if funct(x) >= funct(_x):
                return(x)

    def vnd(self, x, k_max, objective_function):
        k = 0
        while k <= k_max:
            n_struct = self.neighbour_structs[k]
            _x = self.__best_improvement(x, n_struct, objective_function)
            if objective_function(x) < objective_function(_x):
                x = _x
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

            x_ = self.shake(x, n_struct, objective_function)
            x__ = self.vnd(x_, n_struct, l_max, objective_function)

            if objective_function(x) < objective_function(x__):
                x = _x
                k = 0 #reinicializa
            else:
                k = k + 1 #muda estrutura
        return x
