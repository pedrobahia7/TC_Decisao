from neighbour_structs import NeighbourStructs
from metaheuristics import GVNS
from functions import f_C, f_E
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
    cost = df
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
t_max = 5*60

m_recursos_necessarios = pd.read_csv('data_5x50_a.csv', header=None)
m_custo_tarefa = pd.read_csv('data_5x50_c.csv', header=None)
v_capacidade_maxima = pd.read_csv('data_5x50_b.csv', header=None)

gvns = GVNS(
    n=n,
    m=m,
    m_recursos_necessarios = m_recursos_necessarios ,
    v_capacidade_max = v_capacidade_maxima,
    neighbour_structs = NeighbourStructs().structs 
)


for i in range(5):
    x_C = fc_initial_solution(m_custo_tarefa)
    x_E = fe_initial_solution(m_recursos_necessarios)
    solution_C = gvns.gvns(x_C, l_max, k_max, t_max, f_C)
    solution_E = gvns.gvns(x_E, l_max, k_max, t_max, f_E)
    print(f"\n\n-----------Solutions {i}--------\n\n")
    print(solution_C)
    print(solution_E)
