cd nvt
mkdir log
sbatch submit_nvt.sh

# wait ...

sh prep_nve.sh

# and then let's go

mkdir 00/log
cd 00; sbatch submit_gk.sh; cd ..
mkdir 01/log
cd 01; sbatch submit_gk.sh; cd ..
mkdir 02/log
cd 02; sbatch submit_gk.sh; cd ..
mkdir 03/log
cd 03; sbatch submit_gk.sh; cd ..
mkdir 04/log
cd 04; sbatch submit_gk.sh; cd ..
mkdir 05/log
cd 05; sbatch submit_gk.sh; cd ..
mkdir 06/log
cd 06; sbatch submit_gk.sh; cd ..
mkdir 07/log
cd 07; sbatch submit_gk.sh; cd ..
mkdir 08/log
cd 08; sbatch submit_gk.sh; cd ..
mkdir 09/log
cd 09; sbatch submit_gk.sh; cd ..
mkdir 10/log
cd 10; sbatch submit_gk.sh; cd ..

mkdir log
sbatch maxsteps.sh 00
sbatch maxsteps.sh 01
sbatch maxsteps.sh 02
sbatch maxsteps.sh 03
sbatch maxsteps.sh 04
sbatch maxsteps.sh 05
sbatch maxsteps.sh 06
sbatch maxsteps.sh 07
sbatch maxsteps.sh 08
sbatch maxsteps.sh 09
sbatch maxsteps.sh 10

# if things go wrong

rm -r 00
rm -r 01
rm -r 02
rm -r 03
rm -r 04
rm -r 05
rm -r 06
rm -r 07
rm -r 08
rm -r 09
rm -r 10
