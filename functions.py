def f_C(cost,x): #TODO
    final_cost = cost.mul(x).sum().sum()
    return(final_cost)

def f_E(resource,x): #TODO
    CRA = resource.mul(x).sum(axis=1)
    final_consumption = max(CRA) - min(CRA)
    return(final_consumption)

