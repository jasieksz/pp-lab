#!/usr/bin/env python
#%%
from mpi4py import MPI
from typing import Generator
from typing import NoReturn
from typing import Callable
from typing import List
from collections import namedtuple
from functools import partial

#%%
def generate_sizes(base: int, log_length: int) -> Generator:
    return (base**p for p in range(log_length+1)) 

def generate_payload(power_size: int) -> Generator:
    for size in generate_sizes(2, power_size):
        yield bytes(size)

#%%
def send_function(communicator, send_mode: str):
    if (send_mode is 'sync'):
        return lambda data: communicator.ssend(data, dest=1)
    else:
        return lambda data: communicator.send(data, dest=1)

def recevice_function(communicator, source: int):
    return communicator.recv(source=source)

#%%
def get_mpi_communicator():
    return MPI.COMM_WORLD
    
def get_mpi_rank(communicator):
    return communicator.Get_rank()

def mpi_barrier(communicator):
    communicator.Barrier()

def mpi_get_time():
    return MPI.Wtime()

#%%
def runner(communicator, payload_maxsize: int, send: Callable[[bytes], NoReturn], receive: Callable[[int], NoReturn]):
    iterations: int = 100
    rank: int = get_mpi_rank(communicator)
    Measurement = namedtuple('Measurement', 'size, time, iterations')
    results: List[Measurement] = []
    
    for payload in generate_payload(payload_maxsize):
        mpi_barrier(communicator)
        start = mpi_get_time()

        for _ in range(iterations):
            if rank == 0:
                send(payload)
            elif rank == 1:
                receive(0)

        end = mpi_get_time()
        mpi_barrier(communicator)
        results.append(Measurement(len(payload), end-start, iterations))
    
    if rank == 0:
        print('size', 'time', 'iterations', sep=';')
        for r in results:
            print(r.size, r.time, r.iterations, sep=';')
            
 
if __name__ == "__main__":
    communicator = get_mpi_communicator()
    send_regular = partial(send_function, communicator, 'reg')
    send_sync = partial(send_function, communicator, 'sync')
    receive = partial(recevice_function, communicator)
    runner(communicator, 10, send_regular, receive)
