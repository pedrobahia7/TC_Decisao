from neighbour_structs import NeighbourStructs
from metaheuristics import GVNS
from functions import *
import pandas as pd
import numpy as np 

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


n = 5
m = 50

l_max = 2
k_max = 3
t_max = 60

m_recursos_necessarios = pd.read_csv('data_5x50_a.csv', header=None)
m_custo_tarefa = pd.read_csv('data_5x50_c.csv', header=None)
v_capacidade_maxima = pd.read_csv('data_5x50_b.csv', header=None)

gvns = GVNS(
    m_recursos_necessarios = m_recursos_necessarios,
    m_custo_tarefa = m_custo_tarefa,
    v_capacidade_max = v_capacidade_maxima,
    neighbour_structs = NeighbourStructs().structs 
)


for i in range(5):
    x_C = fc_initial_solution(m_custo_tarefa)
    x_E = fe_initial_solution(m_recursos_necessarios)

    x_C.to_csv(f'xc_{i}.csv')
    x_E.to_csv(f'xe_{i}.csv')


    print(f"-----------FC {i}--------")
    solution_C = gvns.gvns(x_E, l_max, k_max, t_max, neg_f_C)

    df_evolution = pd.DataFrame(gvns.evolution_of_f)
    df_evolution.to_csv(f'evolution_of_fc_{i}.csv')
    gvns.evolution_of_f = list()


    print(f"-----------FE {i}--------")
    solution_E = gvns.gvns(x_E, l_max, k_max, t_max, neg_f_E)


    df_evolution = pd.DataFrame(gvns.evolution_of_f)
    df_evolution.to_csv(f'evolution_of_fe_{i}.csv')
    gvns.evolution_of_f = list()


    print(f"\n\n-----------Solutions {i}--------\n\n")
    print("fc(x_C): ", f_C(x_C, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))
    print("fc(solution_C): ", f_C(solution_C, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))

    print("fe(x_E): ", f_E(x_E, m_recursos_necessarios, v_capacidade_maxima, m_recursos_necessarios))
    print("fe(solution_E): ", f_E(solution_E, m_recursos_necessarios, v_capacidade_maxima, m_recursos_necessarios))

    solution_C.to_csv(f'fc_{i}.csv')
    solution_E.to_csv(f'fe_{i}.csv')
