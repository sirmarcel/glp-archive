cd ..
mkdir results

cd results/
rsync -rL --exclude "__pycache__/" --exclude ".DS_Store" --exclude "tf_1*" --exclude ".git" --exclude ".gitignore" --exclude "archive" --exclude ".envrc" --exclude ".gitattributes" --exclude "gaas*" --exclude "mgo*" --exclude "zro*"  --exclude "si*" --exclude "*_stress_and_heat_flux_glp_revision" ../../glp-results/* .
