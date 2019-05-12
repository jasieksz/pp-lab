#!/bin/bash -l

#SBATCH -N 1
#SBATCH --cpus-per-task=12
#SBATCH --time=30:00:00 
#SBATCH -p plgrid
#SBATCH --output="output.out"
#SBATCH --error="error.err"
 
srun /bin/hostname
 
module load plgrid/tools/python/2.7.9
module add plgrid/tools/impi
 
cd $SLURM_SUBMIT_DIR
 
for size in {6..8}
do
    for proc in {1..12}
    do
        mpiexec -np $proc ./py2_pi.py $size regular >> res_reg.txt
    done
done

for size in {6..8}
do
    for proc in {1..12}
    do
        mpiexec -np $proc ./py2_pi.py $size scale >> res_scale.txt
    done
done