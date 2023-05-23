from restrictions import capacidade_excedida
import pandas as pd
import numpy as np

def f_C(x, cost, max_capacity, resource,is_epsilon=0,epsilon=10000): 
    if capacidade_excedida(x, resource, max_capacity) or ( is_epsilon == 1 and f_E(x,cost,max_capacity,resource)>epsilon):
        return 2000
    final_cost = cost.mul(x).sum().sum()
    return(final_cost)

def f_E(x, cost, max_capacity, resource,is_epsilon=0,epsilon=10000):  
    if capacidade_excedida(x, resource, max_capacity) or ( is_epsilon == 1 and f_C(x,cost,max_capacity,resource)>epsilon):
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


def fc_initial_solution(df):
    x = pd.DataFrame(np.zeros(df.shape))
    min_idx = df.idxmin()
    min_idx = min_idx.values.reshape(1,df.shape[1])
    for col in df.columns:
        x.loc[min_idx[0][col],col] = 1
    return(x)

def fe_initial_solution(df):
    cost = df.copy()
    machine_vec = np.zeros(5)
    x = pd.DataFrame(np.zeros(cost.shape))
    cost_copy = cost.copy()
    

    while cost.empty == False:

        min_value = cost_copy.min().min()    
        min_col = cost_copy.min().idxmin()  #task
        min_row = cost_copy.idxmin().loc[min_col] #machine

        if machine_vec[min_row] == 0:
            x.loc[min_row,min_col] = 1 
            machine_vec[min_row] = 1
            cost.drop(min_col,axis = 1, inplace=True)
            cost_copy.drop(min_col,axis = 1, inplace=True)
            if machine_vec.sum() == 5:
                machine_vec = np.zeros(5)
                cost_copy = cost.copy()

        if machine_vec[min_row] == 1:
            cost_copy.loc[min_row,min_col] = 80000000

    return(x)





