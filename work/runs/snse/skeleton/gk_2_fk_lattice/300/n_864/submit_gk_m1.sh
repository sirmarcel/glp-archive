#!/bin/bash -l

#SBATCH -J md|snse:nve:300:864
#SBATCH -o log/md.%j
#SBATCH -e log/md.%j
#SBATCH -D ./
#SBATCH --mail-type=none
#SBATCH --mail-user=langer@fhi-berlin.mpg.de
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --ntasks-per-core=1
#SBATCH -t 12:00:00
#SBATCH --partition=p.talos

cd /u/mlang/glp/; source env.sh; cd -

gkx run md gk_m1.yaml
gkx out gk trajectory/