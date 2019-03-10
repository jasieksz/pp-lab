#!/usr/bin/env bash

set -x

mpiexec  -machinefile ./same_host -np 2 ./timer.py | tee results/1_shm_host.txt
MPIR_CVAR_CH3_NOLOCAL=1 mpiexec  -machinefile ./same_host -np 2 ./timer.py | tee results/2_net_host.txt
MPIR_CVAR_CH3_NOLOCAL=1 mpiexec  -machinefile ./same_machine -np 2 ./timer.py | tee results/3_net_machine.txt
MPIR_CVAR_CH3_NOLOCAL=1 mpiexec -machinefile ./different_machines -np 2 ./timer.py | tee results/4_net_diff.txt