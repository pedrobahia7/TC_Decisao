from neighbour_structs import NeighbourStructs
from metaheuristics import GVNS
from functions import *
import pandas as pd
import numpy as np 

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
    solution_C = gvns.gvns(x_E, l_max, k_max, t_max, f_C)

    df_evolution = pd.DataFrame(gvns.evolution_of_f)
    df_evolution.to_csv(f'evolution_of_fc_{i}.csv')
    gvns.evolution_of_f = list()


    print(f"-----------FE {i}--------")
    solution_E = gvns.gvns(x_E, l_max, k_max, t_max, f_E)


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
