#!/bin/bash -l

#SBATCH -J maxsteps:{{ temperature }}.{{ size }}
#SBATCH -o log/maxsteps.%j
#SBATCH -e log/maxsteps.%j
#SBATCH -D ./
#SBATCH --mail-type=none
#SBATCH --mail-user=langer@fhi-berlin.mpg.de
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --ntasks-per-core=1
#SBATCH -t 00:10:00
#SBATCH --partition=p.talos
cd /u/mlang/glp/; source env.sh; cd -
        
cd $1/
mkdir maxsteps
{% for maxsteps in maxstepss %}
gkx out gk --freq 1.0 --maxsteps {{maxsteps}} -o maxsteps/gk.nc trajectory/
{% endfor %}
cd ../../
