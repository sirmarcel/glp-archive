plot: eos.csv
	eos_fit_data eos.csv --plot

eos.csv:
	eos_get_data eos/*/relaxation/trajectory.son --format vibes

eos:
	python ../create_samples.py
	

