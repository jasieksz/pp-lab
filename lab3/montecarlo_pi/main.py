#!/usr/bin/env python2

import sys
from numpy import random
from mpi4py import MPI

def points_inside_circle(iterations: int) -> int:
    inside_circle = 0
    for _ in range(iterations):
        point = random.random_sample(2)
        if point[0]**2 + point[1]**2 < 1.0:
                inside_circle += 1
    return inside_circle

def measure(comm, rank, n_per_worker: int):
    inside_circle: int = 0
    comm.Barrier()
    start_time: int = MPI.Wtime()

    inside_circle = points_inside_circle(n_per_worker)
    comm.reduce(inside_circle, op=MPI.SUM, root=0)

    end_time = MPI.Wtime()
    if rank == 0:
        print()
        return (end_time - start_time)

def run(n_power: int, mode: str):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if mode == 'regular':
        return (mode, n_power, measure(comm, rank, (10**n_power // size)))
    else:
        return (mode, n_power, measure(comm, rank, 10**n_power))

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(run(int(sys.argv[1]), sys.argv[2]))
    else:
        print(run(6, "regular"))
        