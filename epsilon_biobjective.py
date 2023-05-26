from neighbour_structs import NeighbourStructs
from metaheuristics import GVNS
from functions import *
import pandas as pd
import matplotlib.pyplot as plt

def check_frontier(fe,fc):
    fc_accept_list = list()
    fe_accept_list = list()
    fc_reject_list = list()
    fe_reject_list = list()
    for i in range(len(fe)):
        domination_flag = 0 

        for j in range(len(fe)):
            if (fe[i] > fe[j] and fc[i] > fc[j]):
                domination_flag = 1

        if domination_flag == 0:
            fc_accept_list.append(fc[i])
            fe_accept_list.append(fe[i])


        if domination_flag == 1:
            
            fe_reject_list.append(fe[i])
            fc_reject_list.append(fc[i])

    return(fe_accept_list,fc_accept_list,fe_reject_list,fc_reject_list)
                


is_epsilon = 1


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
                neighbour_structs = NeighbourStructs().structs,
                is_epsilon = is_epsilon,
                ) 




x_C = fc_initial_solution(m_recursos_necessarios)
max_epsilon = int(f_C(x_C, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))
list_of_lists = list()

for i in range(5):
        frontier = list()
        for aux in range(20):
                
                fe_epsilon = max_epsilon - 60*aux
                print(f'epsilon = {fe_epsilon}')
                

                
                x_E = fe_initial_solution(m_recursos_necessarios)
                gvns.epsilon = fe_epsilon

                solution_E = gvns.gvns(x_E, l_max, k_max, t_max, f_E)
                frontier.append(solution_E)
        list_of_lists.append(frontier)


fc0 = list()
fe0 = list()
for i in list_of_lists[0]:
    fc0.append(f_C(i, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))
    fe0.append(f_E(i, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))
fc1 = list()
fe1 = list()
for i in list_of_lists[1]:
    fc1.append(f_C(i, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))
    fe1.append(f_E(i, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))
fc2 = list()
fe2 = list()
for i in list_of_lists[2]:
    fc2.append(f_C(i, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))
    fe2.append(f_E(i, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))
fc3 = list()
fe3 = list()
for i in list_of_lists[3]:
    fc3.append(f_C(i, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))
    fe3.append(f_E(i, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))
fc4 = list()
fe4 = list()
for i in list_of_lists[4]:
    fc4.append(f_C(i, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))
    fe4.append(f_E(i, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios))


fe0_no_dom,fc0_no_dom,none,none = check_frontier(fe0,fc0)
fe1_no_dom,fc1_no_dom,none,none = check_frontier(fe1,fc1)
fe2_no_dom,fc2_no_dom,none,none = check_frontier(fe2,fc2)
fe3_no_dom,fc3_no_dom,none,none = check_frontier(fe3,fc3)
fe4_no_dom,fc4_no_dom,none,none = check_frontier(fe4,fc4)

plt.scatter(fe0_no_dom,fc0_no_dom)
plt.scatter(fe1_no_dom,fc1_no_dom,marker='x')
plt.scatter(fe2_no_dom,fc2_no_dom,marker='v')
plt.scatter(fe3_no_dom,fc3_no_dom,marker='s')
plt.scatter(fe4_no_dom,fc4_no_dom,marker='*')
plt.xlabel('f_E')
plt.ylabel('f_C')
plt.title("Fronteira gerada sem soluções dominadas")
plt.savefig('fronteira_free')

plt.scatter(fe0,fc0)
plt.scatter(fe1,fc1,marker='x')
plt.scatter(fe2,fc2,marker='v')
plt.scatter(fe3,fc3,marker='s')
plt.scatter(fe4,fc4,marker='*')
plt.xlabel('f_E')
plt.ylabel('f_C')
plt.title("Fronteira gerada com soluções dominadas")
plt.savefig('fronteira_dominadas')