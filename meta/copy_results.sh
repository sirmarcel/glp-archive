cd ..
mkdir results

cd results/
rsync -rL --exclude "__pycache__/" --exclude "tf_1*" --exclude ".git" --exclude ".gitignore" --exclude "archive" --exclude ".envrc" --exclude ".gitattributes" --exclude "gaas*" ../../glp-results/* .
