from neighbour_structs import NeighbourStructs
from metaheuristics import GVNS
import pandas as pd
import numpy as np 



gvns = GVNS( NeighbourStructs().structs )



def fc_initial_solution(resources):
    x = pd.DataFrame(np.zeros(resources.shape))
    min_idx = resources.idxmin()
    min_idx = min_idx.values.reshape(1,resources.shape[1])
    for col in resources.columns:
        x.loc[min_idx[0][col],col] = 1
    return(x)





for i in range(5):
    solution_C = gvns.gvns(x, f_C)
    solution_E = gvns.gvns(x, f_E)
    print(f"\n\n-----------Solutions {i}--------\n\n")
    print(solution_C)
    print(solution_E)
