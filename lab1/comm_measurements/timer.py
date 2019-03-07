#!/usr/bin/env python
#%%
from typing import List
from mpi4py import MPI
from functools import partial

#%%
def generate_sizes(base: int, log_length: int) -> List[int]:
    return [base**p for p in range(log_length)]

#%%
def send_function(communicator, send_mode) -> function:
    if (send_mode is 'sync'):
        return lambda data: communicator.ssend(data, dest=1)
    else:
        return lambda data: communicator.send(data, dest=1)

#%%
comm = MPI.COMM_WORLD
send_regular_func = partial(send_function, comm, 'reg')
send_sync_func = partial(send_function, comm, 'sync')