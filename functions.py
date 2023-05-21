from restrictions import capacidade_excedida

def f_C(x, cost, max_capacity, resource): 
    if capacidade_excedida(x, resource, max_capacity):
        return 2000
    final_cost = cost.mul(x).sum().sum()
    return(final_cost)

def f_E(x, cost, max_capacity, resource): 
    if capacidade_excedida(x, resource, max_capacity):
        return 200
    CRA = resource.mul(x).sum(axis=1)
    final_consumption = max(CRA) - min(CRA)
    return(final_consumption)

def neg_f_C(x, cost, max_capacity, resource): 
    if capacidade_excedida(x, resource, max_capacity):
        return 2000
    final_cost = cost.mul(x).sum().sum()
    return(-final_cost)

def neg_f_E(x, cost, max_capacity, resource): 
    if capacidade_excedida(x, resource, max_capacity):
        return 200
    CRA = resource.mul(x).sum(axis=1)
    final_consumption = max(CRA) - min(CRA)
    return(-final_consumption)

