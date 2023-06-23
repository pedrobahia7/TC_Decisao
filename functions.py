from restrictions import capacidade_excedida
from math import sqrt
import pandas as pd
import numpy as np
import random

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

def criterio_variacao_em_c(x, cost, max_capacity, resource):
    new_cost = cost.copy()
    for i in range(3):
        col1, col2 = random.sample(range(50), 2)
        new_cost[col1], new_cost[col2] = cost[col2], cost[col1]

    old_E = f_E(x, cost, max_capacity, resource)
    old_C = f_C(x, cost, max_capacity, resource)

    new_E = f_E(x, new_cost, max_capacity, resource)
    new_C = f_C(x, new_cost, max_capacity, resource)

    return sqrt((new_E - old_E)**2 + (new_C - old_C)**2)

def criterio_variacao_em_a(x, cost, max_capacity, resource):
    new_resource = resource.copy()
    for i in range(3):
        col1, col2 = random.sample(range(50), 2)
        new_resource[col1], new_resource[col2] = resource[col2], resource[col1]

    old_E = f_E(x, cost, max_capacity, resource)
    old_C = f_C(x, cost, max_capacity, resource)

    new_E = f_E(x, cost, max_capacity, new_resource)
    new_C = f_C(x, cost, max_capacity, new_resource)

    return sqrt((new_E - old_E)**2 + (new_C - old_C)**2)
