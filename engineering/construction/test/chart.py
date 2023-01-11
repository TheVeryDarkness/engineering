import pathlib

sd = pathlib.Path(__file__)
p = sd.parent
from .. import chart


def main():
    with open(str(p / "mooc-1.svg"), "w", encoding="UTF-8") as f:
        chart.accelerated_beat_flow(4, [], [4, 10, 12], "d", f, False)
    with open(str(p / "mooc-1-v.svg"), "w", encoding="UTF-8") as f:
        chart.accelerated_beat_flow(4, [], [4, 10, 12], "d", f, True)

    with open(str(p / "textbook-11-1.svg"), "w", encoding="UTF-8") as f:
        chart.accelerated_beat_flow(
            4, ["基础工程", "结构安装", "室内装修", "室外工程"], [5, 10, 10, 5], "周", f, False
        )
    with open(str(p / "textbook-11-1-v.svg"), "w", encoding="UTF-8") as f:
        chart.accelerated_beat_flow(
            4, ["基础工程", "结构安装", "室内装修", "室外工程"], [5, 10, 10, 5], "周", f, True
        )

    with open(str(p / "textbook-11-1-n.svg"), "w", encoding="UTF-8") as f:
        chart.normal_beat_flow(
            4, ["基础工程", "结构安装", "室内装修", "室外工程"], [5, 10, 10, 5], "周", f, False
        )
    with open(str(p / "textbook-11-1-n-v.svg"), "w", encoding="UTF-8") as f:
        chart.normal_beat_flow(
            4, ["基础工程", "结构安装", "室内装修", "室外工程"], [5, 10, 10, 5], "周", f, True
        )

    with open(str(p / "textbook-11-2-n.svg"), "w", encoding="UTF-8") as f:
        chart.non_beat_flow(
            6,
            [],
            [[3, 3, 2, 2, 2, 2], [4, 2, 3, 2, 2, 3], [2, 2, 3, 3, 3, 2]],
            "周",
            f,
            False,
        )
    with open(str(p / "textbook-11-2-n-v.svg"), "w", encoding="UTF-8") as f:
        chart.non_beat_flow(
            6,
            [],
            [[3, 3, 2, 2, 2, 2], [4, 2, 3, 2, 2, 3], [2, 2, 3, 3, 3, 2]],
            "周",
            f,
            True,
        )

    with open(str(p / "practice-11-5-n.svg"), "w", encoding="UTF-8") as f:
        chart.non_beat_flow(
            4,
            [],
            [[4, 3, 1, 2], [2, 3, 4, 2], [3, 4, 2, 1], [2, 4, 5, 2]],
            "单位",
            f,
            False,
        )
    with open(str(p / "practice-11-5-n-v.svg"), "w", encoding="UTF-8") as f:
        chart.non_beat_flow(
            4,
            [],
            [[4, 3, 1, 2], [2, 3, 4, 2], [3, 4, 2, 1], [2, 4, 5, 2]],
            "单位",
            f,
            True,
        )

    with open(str(p / "practice-11-7-n.svg"), "w", encoding="UTF-8") as f:
        chart.non_beat_flow(
            4,
            [],
            [[3, 4, 3, 2], [5, 6, 4, 5], [5, 4, 5, 5], [7, 2, 6, 1]],
            "单位",
            f,
            False,
        )
    with open(str(p / "practice-11-7-n-v.svg"), "w", encoding="UTF-8") as f:
        chart.non_beat_flow(
            4,
            [],
            [[3, 4, 3, 2], [5, 6, 4, 5], [5, 4, 5, 5], [7, 2, 6, 1]],
            "单位",
            f,
            True,
        )
