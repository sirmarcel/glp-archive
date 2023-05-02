from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import shutil

temperatures = [300]
sizes = [256, 864, 2048, 4000, 6912]

size_to_skin = {256: 1.0, 864: 1.0, 2048: 1.0, 4000: 1.0, 6912: 1.0}
size_to_skin_unfolder = {256: 2.0, 864: 2.0, 2048: 2.0, 4000: 2.0, 6912: 2.0}

environment = Environment(loader=FileSystemLoader("templates/"))


def make_temperature(temperature):
    folder = Path(f"{temperature}")

    folder.mkdir(exist_ok=True)

    for size in sizes:
        f = folder / f"n_{size}"
        f.mkdir(exist_ok=True)

        (f / "nvt").mkdir(exist_ok=True)
        write_md_nvt(f, temperature, size)

        write_md_nve(f, temperature, size)


def write_md_nvt(folder, temperature, size):
    render(
        "nvt.yaml",
        {"temperature": temperature, "size": size, "skin": size_to_skin[size]},
        folder / "nvt/nvt.yaml",
    )

    render(
        "submit_nvt.sh",
        {"temperature": temperature, "size": size, "skin": size_to_skin[size]},
        folder / "nvt/submit_nvt.sh",
    )

    shutil.copy(
        f"cells/geometry.in.primitive.supercell_{size}.0300K",
        folder / "nvt/geometry.in",
    )

    shutil.copy(
        f"cells/geometry.in.primitive.supercell_{size}",
        folder / "nvt/geometry.in.supercell",
    )

    shutil.copy(
        f"cells/geometry.in.primitive",
        folder / "nvt/geometry.in.primitive",
    )


def write_md_nve(folder, temperature, size):
    render(
        "gk.yaml",
        {
            "temperature": temperature,
            "size": size,
            "skin": size_to_skin[size],
            "skin_unfolder": size_to_skin_unfolder[size],
        },
        folder / "gk.yaml",
    )
    render(
        "gk_m1.yaml",
        {
            "temperature": temperature,
            "size": size,
            "skin": size_to_skin[size],
        },
        folder / "gk_m1.yaml",
    )

    render(
        "submit_gk.sh",
        {
            "temperature": temperature,
            "size": size,
        },
        folder / "submit_gk.sh",
    )

    render(
        "submit_gk_m1.sh",
        {
            "temperature": temperature,
            "size": size,
        },
        folder / "submit_gk_m1.sh",
    )

    shutil.copy(
        f"templates/prep_nve.py",
        folder / "prep_nve.py",
    )
    shutil.copy(
        f"templates/prep_nve.sh",
        folder / "prep_nve.sh",
    )

    maxstepss = list(range(25000, 1000001, 25000))
    render(
        "maxsteps.sh",
        {
            "temperature": temperature,
            "size": size,
            "maxstepss": maxstepss,
        },
        folder / "maxsteps.sh",
    )


def render(template, arguments, outfile):
    with open(outfile, "w") as f:
        f.write(environment.get_template(template).render(arguments))


for t in temperatures:
    make_temperature(t)
