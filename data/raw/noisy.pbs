#!/bin/bash
#PBS -q workq
#PBS -N zdt-noizy
#PBS -P PR350
#PBS -o noisy-out.txt
#PBS -e noisy-err.txt
#PBS -l select=1:ncpus=16:mpiprocs=16
#PBS -l place=scatter:excl
#PBS -l walltime=70:00:00

export MPLBACKEND="agg"

# Install local code
cd /scratch/smavak/testing_for_ZD
/home/smavak/anaconda3/envs/testing-zd/bin/python setup.py develop

# Run experiment
cd data/raw
/home/smavak/anaconda3/envs/testing-zd/bin/python main.py noisy full
/home/smavak/anaconda3/envs/testing-zd/bin/python main.py noisy stewart_plotkin
