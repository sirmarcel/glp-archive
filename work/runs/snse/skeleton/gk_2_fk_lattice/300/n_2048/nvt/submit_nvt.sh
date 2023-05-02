#!/bin/bash -l

#SBATCH -J md|snse:nvt:300:2048
#SBATCH -o log/md.%j
#SBATCH -e log/md.%j
#SBATCH -D ./
#SBATCH --mail-type=none
#SBATCH --mail-user=langer@fhi-berlin.mpg.de
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --ntasks-per-core=1
#SBATCH -t 24:00:00
#SBATCH --partition=p.talos

cd /u/mlang/glp/; source env.sh; cd -

gkx run md nvt.yaml