cd ..
mkdir work

cp meta/README_work.md work/README.md

cd work/

mkdir runs
cd runs
mkdir snse
cd snse
mkdir skeleton
cd skeleton
rsync -r ../../../../../glp-work/runs/snse/skeleton/gk_2_fk_lattice .
rsync -r ../../../../../glp-work/runs/snse/skeleton/phonons .
rsync -r ../../../../../glp-work/runs/snse/skeleton/vdos .

cd ..
rsync -r --exclude "archive" ../../../../glp-work/runs/snse/reference .

cd ../../

mkdir experiments
cd experiments

rsync -r --exclude "__pycache__/" --exclude ".DS_Store" --exclude "model" --exclude "new_glp_lj_mk04" --exclude "new_glp_production_models_train_default_L2" ../../../glp-work/experiments/implementation_stress_and_heat_flux .
rsync -r --exclude "__pycache__/" --exclude ".DS_Store" --exclude "model" ../../../glp-work/experiments/time_stress_and_heat_flux .
rsync -r --exclude "__pycache__/" --exclude ".DS_Store" ../../../glp-work/experiments/EOS .

cd ..
mkdir models
cd models

rsync -r --exclude "__pycache__/" --exclude ".DS_Store" ../../../glp-work/models/production_models .
