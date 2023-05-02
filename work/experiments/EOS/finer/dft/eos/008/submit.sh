#!/bin/bash -l

#SBATCH -J relaxation|dardel
#SBATCH -o log/relaxation.%j
#SBATCH -e log/relaxation.%j
#SBATCH -D ./
#SBATCH --mail-type=all
#SBATCH --mail-user=florian.knoop@liu.se
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --ntasks-per-core=1
#SBATCH -t 0:30:00
#SBATCH --partition=main

source activate vibes
vibes run relaxation relaxation.in
