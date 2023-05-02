#!/bin/bash -l

train_so3krates \
	--L 3 \
	--epochs 2500 \
	--n_train 2400 \
	--n_valid 600 \
	--mic \
	--data_file ../mlff_data.npz \
	--targets energy force \
	--loss_weights energy=0.01,force=1 \
	--wandb_init project=so3krates,group=SnSe_production

