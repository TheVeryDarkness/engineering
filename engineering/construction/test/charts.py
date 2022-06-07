import pathlib
import os
import sys

sd = pathlib.Path(__file__)
p = sd.parent
from .. import chart

if __name__ == "__main__":
    with open(str(p / "mooc-1.svg"), "w", encoding="UTF-8") as f:
        chart.fast_pipeline(4, [], [4, 10, 12], "d", f, False)
    with open(str(p / "mooc-1-v.svg"), "w", encoding="UTF-8") as f:
        chart.fast_pipeline(4, [], [4, 10, 12], "d", f, True)

    with open(str(p / "textbook-11-1.svg"), "w", encoding="UTF-8") as f:
        chart.fast_pipeline(
            4, ["基础工程", "结构安装", "室内装修", "室外工程"], [5, 10, 10, 5], "周", f, False
        )
    with open(str(p / "textbook-11-1-v.svg"), "w", encoding="UTF-8") as f:
        chart.fast_pipeline(
            4, ["基础工程", "结构安装", "室内装修", "室外工程"], [5, 10, 10, 5], "周", f, True
        )
