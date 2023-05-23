from neighbour_structs import NeighbourStructs
from metaheuristics import GVNS
from functions import *
import pandas as pd
import numpy as np 
import random as rd

def check_frontier(solution,frontier):

    [aux_fc, aux_fe] = [f_C(solution, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios), f_E(solution, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios)]
    is_append = 1
    remove_list = list()
    for i in range(len(frontier)):
        if solution == frontier[i]:
            break
        aux = 0 
        if f_C(frontier[i], m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios) > aux_fc:
            aux = aux +1 
            
        if f_E(frontier[i], m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios) > aux_fe:
            aux = aux +1

        if aux == 2:
            remove_list.append(frontier[i])
            
        elif aux == 0:
            is_append = 0

    
    for i in remove_list:
        frontier = frontier.remove(i)
        if frontier == None:
            frontier = list()
        
    if is_append==1:
        frontier.append(solution)
        

is_epsilon = 1


n = 5
m = 50

l_max = 2
k_max = 3
t_max = 60

m_recursos_necessarios = pd.read_csv('data_5x50_a.csv', header=None)
m_custo_tarefa = pd.read_csv('data_5x50_c.csv', header=None)
v_capacidade_maxima = pd.read_csv('data_5x50_b.csv', header=None)

list_of_lists = list()
#for aux in range(1):
frontier = list()
while len(frontier) < 15:
        
    fc_epsilon = rd.randrange(1200, 1800)

    gvns = GVNS(
    m_recursos_necessarios = m_recursos_necessarios,
    m_custo_tarefa = m_custo_tarefa,
    v_capacidade_max = v_capacidade_maxima,
    neighbour_structs = NeighbourStructs().structs,
    is_epsilon = is_epsilon,
    epsilon = fc_epsilon
    ) 

    
    x_E = fe_initial_solution(m_recursos_necessarios)



    

    

    
    gvns.epsilon = fc_epsilon


    solution_E = gvns.gvns(x_E, l_max, k_max, t_max, f_E)
    check_frontier(solution_E,frontier)
    list_of_lists.append(frontier)


