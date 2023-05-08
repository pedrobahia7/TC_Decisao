import itertools

class NeighbourStructs():
    def __init__(self):
        self.structs = [
            self.swap_lines, 
            self.swap_solution, 
            self.swap_columns, 
        ]

    def swap_lines(x): 
        perms = itertools.permutations(range(len(x)), 2)
        neighbours = []
        for perm in perms:
            new_neighbour = x.copy()
            row1, row2 = perm
            new_neighbour.iloc[row1], new_neighbour.iloc[row2] = x.iloc[row2], x.iloc[row1]
            neighbours.append(new_neighbour)

    def swap_solution(): #TODO
        pass

    def swap_columns(x): #TODO
        perms = itertools.permutations(range(len(x.columns)), 2)
        neighbours = []
        for perm in perms:
            new_neighbour = x.copy()
            col1, col2 = perm
            new_neighbour[col1], new_neighbour[col2] = x[col2], x[col1]
            neighbours.append(new_neighbour)
