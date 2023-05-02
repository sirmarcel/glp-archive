import xarray as xr


def ensemble(folder, subfolder, file, n=11):
    datasets = []

    enss = [f"{i:02d}" for i in range(n)]
    for ens in enss:
        dataset = ((folder / ens) / subfolder) / file

        datasets.append(xr.open_dataset(dataset))

    return datasets
