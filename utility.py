import numpy as np
def printsol(message,sol):
    sol_print=np.zeros_like(sol,dtype=int)
    for i in range(len(sol)):
        for j in range(len(sol[i])):
            sol_print[i,j]=sol[i,j].x
            
    print(message)
    print(sol_print)

def toMatrix(sol):
    sol_print=np.zeros_like(sol,dtype=int)
    for i in range(len(sol)):
        for j in range(len(sol[i])):
            sol_print[i,j]=sol[i,j].x
    return sol_print

def toArray(sol):
    sol_print=np.zeros_like(sol,dtype=int)
    for i in range(len(sol)):    
        sol_print[i]=sol[i].x
    return sol_print

