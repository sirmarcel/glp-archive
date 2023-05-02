#!/bin/bash -l

#SBATCH -J maxsteps:300.864
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

gkx out gk --freq 1.0 --maxsteps 25000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 50000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 75000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 100000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 125000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 150000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 175000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 200000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 225000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 250000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 275000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 300000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 325000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 350000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 375000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 400000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 425000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 450000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 475000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 500000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 525000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 550000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 575000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 600000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 625000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 650000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 675000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 700000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 725000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 750000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 775000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 800000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 825000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 850000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 875000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 900000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 925000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 950000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 975000 -o maxsteps/gk.nc trajectory/

gkx out gk --freq 1.0 --maxsteps 1000000 -o maxsteps/gk.nc trajectory/

cd ../../