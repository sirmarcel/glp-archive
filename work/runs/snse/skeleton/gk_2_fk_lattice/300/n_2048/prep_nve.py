from pathlib import Path
import shutil
from ase.io import write
from stepson.trajectory import Trajectory

spacing = (40000, 50001, 1000)
starts = list(reversed(range(*spacing)))
gk_run_names = list(map(lambda x: f"{x:02d}", range(len(starts))))

nvt = Trajectory("nvt/trajectory/")

for i, name in enumerate(gk_run_names):
    offset = starts[i]
    atoms = nvt.get_atoms(offset-1)

    folder = Path(name)
    folder.mkdir(exist_ok=True)

    write(
        folder / "geometry.in",
        atoms,
        format="aims",
        scaled=True,
        velocities=True,
        info_str=f"NVT sample {offset}",
    )
    shutil.copy("nvt/geometry.in.primitive", folder / "geometry.in.primitive")
    shutil.copy("nvt/geometry.in.supercell", folder / "geometry.in.supercell")
    shutil.copy("gk.yaml", folder / "gk.yaml")
    shutil.copy("gk_m1.yaml", folder / "gk_m1.yaml")
    shutil.copy("submit_gk.sh", folder / "submit_gk.sh")
    shutil.copy("submit_gk_m1.sh", folder / "submit_gk_m1.sh")
