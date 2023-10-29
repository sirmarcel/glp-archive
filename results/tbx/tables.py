from copy import deepcopy
from functools import partial


def rounder(digits, typ="f"):
    def formatter(number):
        return "{:.{digits}{typ}}".format(number, digits=digits, typ=typ)

    return formatter


def aligner(width):
    def formatter(s):
        return "{0:>{width}}".format(s, width=width)

    return formatter


def to_num(entry):
    entry = str(entry)
    return r"\num{X}".replace("X", entry)


def map_across(table, fns):
    result = []

    for row in table:
        result.append([fns[i](entry) for i, entry in enumerate(row)])

    return result


def ncols(data):
    return len(data[0])


def table_to_string(
    data, rownames=None, colnames=None, width=10, colsep="|", rowsep="\n"
):
    data = deepcopy(data)

    if rownames is not None:
        for i, rowname in enumerate(rownames):
            data[i].insert(0, rowname)

    if colnames is not None:
        data.insert(0, colnames)

    if isinstance(width, int):
        aligners = [aligner(width) for i in range(ncols(data))]
    else:
        aligners = [aligner(w) for w in width]

    data = map_across(data, aligners)

    strings = []

    for i, row in enumerate(data):
        strings.append(f" {colsep} ".join(row))

    return rowsep.join(strings) + rowsep


table_to_tex = partial(table_to_string, colsep=" & ", rowsep=" \\\\ \n")


def make_tabular(titles, table, layout=None, width=20, heading=None, tables=None):
    if tables is None:
        tables = [table]

    if not _is_nested(titles):
        titles = [titles]

    if layout is None:
        layout = " ".join(["l"] * len(titles))

    out = r"\begin{tabular}{X}".replace("X", layout) + "\n"
    out += r"\toprule" + "\n"
    if heading is not None:
        out += heading

    out += table_to_tex(titles, width=width)

    for table in tables:
        out += r"\midrule" + "\n"
        out += table_to_tex(table, width=width)

    out += r"\bottomrule" + "\n"
    out += r"\end{tabular}" + "\n"

    return out


def _is_nested(l):
    return isinstance(l[0], list)
