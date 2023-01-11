from bidict import bidict


def double_code_network_chart(previous: dict[int, list[int]]):
    names: bidict[int, str] = bidict()
    post: dict[int, list[int]] = {}
    pre: dict[int, list[int]]
