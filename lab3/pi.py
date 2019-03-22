#!/usr/bin/env python
# from mpi4py import MPI

#%%
from numpy import random

#%%
def generate(size=10):
    return random.rand(size*2).reshape((size,2))
    
#%%
def montecarlo_pi(size=100000):
    c = sum(1 for xy in generate(size) if xy[0]**2+xy[1]**2 <= 1)
    return c

#%%
if __name__ == "__main__":       
    comm = MPI.COMM_WORLD

    data = 0
    total = 0

    for i in range(MPI.size):
        data = montecarlo_pi()


    
    data = gen
    comm.Barrier()
    comm.Reduce(
        [data, MPI.INT],
        [total, MPI.INT],
        op = MPI.SUM,
        root = 0
    )


    print '[%i]'%comm.rank, totals





# sprawozdanie HOW TO: 
# dane : 10^x : x=6,9,10
# metoda : nieskalowana
# wykresy : 
#   time, y=1/x
#   speedup (ts/tp), y=x
#   efficiency (speedup / cpu), y=1
#   serial fraction (1/s - 1/t)/(1 - 1/t)

# metoda : skalowana (zwiększamy rozmiar danych?)
# wykresy : 
#   time, y=1
#   speedup (cpu * ts / tp), y=x
#   efficiency (speedup / cpu), y=1
#   serial fraction (1/s - 1/t)/(1 - 1/t)
#     
# nie dawać lini łączącej punkty!!!