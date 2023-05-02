cd ..

rm -r infra
rm -r results
rm -r work

cd meta
sh copy_infra.sh
sh copy_results.sh
sh copy_work.sh