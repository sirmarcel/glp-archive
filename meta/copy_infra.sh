cd ..
mkdir infra

cp meta/README_infra.md infra/README.md

cd infra/
rsync -r --exclude "__pycache__/" --exclude ".git" --exclude ".gitignore" --exclude "gloopy/" ../../glp-infra/* .