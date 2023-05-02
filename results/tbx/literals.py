tol_vibrant = [
    "#EE7733",
    "#0077BB",
    "#33BBEE",
    "#EE3377",
    "#CC3311",
    "#009988",
    "#BBBBBB",
    "#000000",
]

tol_muted = [
    "#88CCEE",
    "#44AA99",
    "#117733",
    "#332288",
    "#DDCC77",
    "#999933",
    "#CC6677",
    "#882255",
    "#AA4499",
    "#DDDDDD",
]

nolabel = "__nolabel__"

orange = "#EE7733"
blue = "#0077BB"
cyan = "#33BBEE"
magenta = "#EE3377"
red = "#CC3311"
teal = "#009988"
grey = "#BBBBBB"
black = "#000000"

solid = "solid"
dashed = "dashed"
dotted = "dotted"
dashdot = "dashdot"
loosedot = (0, (1, 1))
loosedash = ((1, 1), 0)
finedot = (0, (0.5, 2))
finedash = (0, (4, 3))

cross = "x"
diamond = "D"
star = "*"
dot = "."
bigdot = "o"
square = "s"
thiamond = "d"
pentagon = "p"
plus = "P"

sok = r"\textsc{so3krates}"


def wmk(develop=True):
    if develop:
        return "W/mK"
    else:
        return r"\unit{W\per(m.K)}"


def render_kappa(value, develop=True):
    if develop:
        return f"${value:.1f}$ {wmk(develop=True)}"
    else:
        return r"\qty{X}{W\per(m.K)}".replace("X", f"{value:.1f}")


def kappa_label(develop=True):
    if develop:
        return r"$\kappa$ (W/mK)"
    else:
        return r"$\kappa$ (\unit{W\per(m.K)})"


def render_temp(value, develop=True, approx=False):
    if develop:
        if approx:
            return f"~${value}$K"
        else:
            return f"${value}$K"
    else:
        if approx:
            return r"$\sim$ \qty{X}{K}".replace("X", f"{value}")
        else:
            return r"\qty{X}{K}".replace("X", f"{value}")


def render_time(value, develop=True, unit="ns"):
    if develop:
        return f"${value}${unit}"
    else:
        return r"\qty{X}{Y}".replace("X", f"{value}").replace("Y", unit)


def with_stderr(value, err=None):
    if err is not None:
        return r"\num{X \pm Y}".replace("X", str(value)).replace("Y", str(err))
    else:
        return r"\num{X}".replace("X", str(value))
