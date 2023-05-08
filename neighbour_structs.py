import itertools

class NeighbourStructs():
    def __init__(self):
        self.structs = [
            self.swap_lines, 
            self.swap_machines, 
            self.swap_columns, 
        ]

    def swap_lines(self, x): 
        perms = itertools.permutations(range(len(x)), 2)
        neighbours = []
        for perm in perms:
            new_neighbour = x.copy()
            row1, row2 = perm
            new_neighbour.iloc[row1], new_neighbour.iloc[row2] = x.iloc[row2], x.iloc[row1]
            neighbours.append(new_neighbour)
        return neighbours

    def swap_machines(self, x_original):
        x_list = list()
        for col in x_original.columns:
            x = x_original.copy()
            x_one_idx = x.loc[:,col].where(x.loc[:,col]==1).idxmax()
            for row in x.index:
                x = x_original.copy()
                if x.loc[row,col] == 0:
                    x.loc[row,col] = 1
                    x.loc[x_one_idx,col] = 0
                    x_list.append(x)
        return(x_list)    

    def swap_columns(self, x):
        perms = itertools.permutations(range(len(x.columns)), 2)
        neighbours = []
        for perm in perms:
            new_neighbour = x.copy()
            col1, col2 = perm
            new_neighbour[col1], new_neighbour[col2] = x[col2], x[col1]
            neighbours.append(new_neighbour)
        return neighbours
