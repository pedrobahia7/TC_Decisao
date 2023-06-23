from neighbour_structs import NeighbourStructs
from tomador_de_decisao import TomadorDeDecisao
from metaheuristics import GVNS
from functions import *
import pandas as pd
import numpy as np 

n = 5
m = 50

l_max = 2
k_max = 3
t_max = 30

m_recursos_necessarios = pd.read_csv('data_5x50_a.csv', header=None)
m_custo_tarefa = pd.read_csv('data_5x50_c.csv', header=None)
v_capacidade_maxima = pd.read_csv('data_5x50_b.csv', header=None)

gvns = GVNS(
    m_recursos_necessarios = m_recursos_necessarios,
    m_custo_tarefa = m_custo_tarefa,
    v_capacidade_max = v_capacidade_maxima,
    neighbour_structs = NeighbourStructs().structs 
)


all_solutions = []
all_evaluated_solutions = []

for i in range(5):
    x_C = fc_initial_solution(m_custo_tarefa)
    x_E = fe_initial_solution(m_recursos_necessarios)
    #x_C.to_csv(f'xc_{i}.csv')
    #x_E.to_csv(f'xe_{i}.csv')

    result = gvns.soma_ponderada_biobjetivo(x_E, x_E, x_E, l_max, k_max, t_max, f_C, f_E, neg_f_C, neg_f_E)
    for idx,aux in enumerate(result):

        evaluated_solution = (
            f_C(aux, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios),
            f_E(aux, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios),
            criterio_variacao_em_a(aux, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios),
            criterio_variacao_em_c(aux, m_custo_tarefa, v_capacidade_maxima, m_recursos_necessarios),
        )
        if not (evaluated_solution[0] >= 2000 or evaluated_solution[1] >= 200):
            all_evaluated_solutions.append(evaluated_solution)
            all_solutions.append(aux)

w = [
    0.3, 
    0.3, 
    0.2, 
    0.2
]

max_or_min = False
print("-----------------bellzadeh------------------")
(matriz, notas, ordem) = TomadorDeDecisao().bellzadeh(all_evaluated_solutions, w, max_or_min)
np.savetxt("bellzadeh.csv", np.asarray(all_solutions)[ordem], delimiter=",")
np.savetxt("eval_bellzadeh.csv", np.asarray(matriz), delimiter=",")

for idx in range(len(notas)):
    print(f"{tuple(matriz[idx])}:\n\tnota:{notas[idx]}\n")

print("-----------------topsis------------------")

(matriz, notas, ordem) = TomadorDeDecisao().topsis(all_evaluated_solutions, w, max_or_min)
np.savetxt("topsis.csv", np.asarray(all_solutions)[ordem], delimiter=",")
np.savetxt("eval_topsis.csv", np.asarray(matriz), delimiter=",")
for idx in range(5):
    print(f"{tuple(matriz[idx])}:\n\tnota:{notas[idx]}\n")
