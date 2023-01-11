from genericpath import exists
from os import mkdir
import pathlib

sd = pathlib.Path(__file__)
p = sd.parent
from .. import table


def main():
    table.tableManipulationMethod(
        costs=[[50, 70, 100], [70, 40, 90], [60, 110, 70], [80, 100, 40]],
        W=[500, 500, 500, 400],
        T=[800, 600, 500],
        path=lambda i: str(p / f"textbook-1.3.2.3-{i}.svg"),
    )
    if not exists(str(p / "error")):
        mkdir(str(p / "error"))
    try:
        table.tableManipulationMethod(
            costs=[[50, 70], [70, 40]],
            W=[500, 500],
            T=[500, 500],
            path=lambda i: str(p / "error" / f"{i}.svg"),
        )
    except:
        print("表上作业法不总是那么好用。")
