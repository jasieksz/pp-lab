#!/usr/bin/env python2
import sys
import gc
import numpy as np
from mpi4py import MPI

#%%
def gen_lengths(max_len):
    x = 1
    while x < max_len:
        yield int(x)
        if x < 50:
            x += 3
        else:
            x *= 1.14

#%%
if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    results = []
    iterations = 100

    for i in range(3):
        rst = []
        for payload_size in gen_lengths(max_len=(2**22)):

            payload_bytes = bytearray(payload_size)
            gc.collect()

            comm.Barrier()
            start_reg = MPI.Wtime()
            for _ in xrange(iterations):
                if rank == 0:
                    comm.send(payload_bytes, dest=1)
                elif rank == 1:
                    comm.recv(source=0)
            end_reg = MPI.Wtime()

            comm.Barrier()
            start_sync = MPI.Wtime()
            for _ in xrange(iterations):
                if rank == 0:
                    comm.ssend(payload_bytes, dest=1)
                elif rank == 1:
                    comm.recv(source=0)
            end_sync = MPI.Wtime()
            comm.Barrier()

            m_bit_per_second_reg = ((8 * payload_size * iterations)/(end_reg - start_reg)) / 10**6
            m_bit_per_second_sync = ((8 * payload_size * iterations)/(end_sync - start_sync)) / 10**6
            rst.append((payload_size, m_bit_per_second_reg, m_bit_per_second_sync))
        results.append(rst)
        
    if rank == 0:
        x = np.array(results)
        x = np.array(x.transpose().mean(axis=-1)).transpose()
        print 'size;bandwidth(reg);bandwidth(sync)'
        for r in results:
            print '%d;%f;%f' % (r[0], r[1], r[2])
