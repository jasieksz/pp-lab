#!/usr/bin/env python2
import sys
import numpy as np
import random
from mpi4py import MPI

def points_inside_circle(iterations):
    inside_circle = 0
    # local_random = random.Random()
    for _ in range(iterations):
        x, y = random.random(), random.random()
        if x**2 + y**2 < 1.0:
                inside_circle += 1
    return np.array(inside_circle, 'd')

def measure(comm, rank, n_per_worker):
    result = np.array(0.0,'d')
    comm.Barrier()
    start_time = MPI.Wtime()

    inside_circle = points_inside_circle(n_per_worker)
    comm.Reduce(inside_circle, result, op=MPI.SUM, root=0)

    end_time = MPI.Wtime()
    if rank == 0:
        return (end_time - start_time, result)
    else:
	    return (0, 0)

def run(n_power, mode):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if mode == 'regular':
        time, pi = measure(comm, rank, (10**n_power // size))
        if rank == 0:
             print mode, size, n_power, time, (4 * pi / 10**n_power)
    else:
        time, pi = measure(comm, rank, 10**n_power)
        if rank == 0:
           print mode, size, n_power, time, (4 * pi / (10**n_power * size))

if __name__ == "__main__":
    if len(sys.argv) == 3:
        run(int(sys.argv[1]), sys.argv[2])
    else:
        run(6, "regular")
        
