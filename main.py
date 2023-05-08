from neighbour_structs import NeighbourStructs
from metaheuristics import GVNS
import pandas as pd
import numpy as np 



gvns = GVNS( NeighbourStructs().structs )



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






for i in range(5):
    solution_C = gvns.gvns(x, f_C)
    solution_E = gvns.gvns(x, f_E)
    print(f"\n\n-----------Solutions {i}--------\n\n")
    print(solution_C)
    print(solution_E)
