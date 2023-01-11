from itertools import islice
from typing import Callable, TextIO
import copy

__X = 100
__Y = 60
__FONT_SIZE = 20
__MARGIN = 15
__TEXT_PROP = f'font-size="{__FONT_SIZE}"'
__MIDDLE_TEXT_PROP = f'text-anchor="middle" {__TEXT_PROP}'
__EXTRA_Y_OFFSET = 2
__LINE_STYLE = "stroke-width:2;fill:none;"


def __write_text_in_box(
    text: str,
    x1: float | int,
    x2: float | int,
    y1: float | int,
    y2: float | int,
    file: TextIO,
):
    print(
        f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2+__FONT_SIZE/2-__EXTRA_Y_OFFSET}" {__MIDDLE_TEXT_PROP}>{text}</text>',
        file=file,
    )


def __write_line(
    x1: float | int, x2: float | int, y1: float | int, y2: float | int, file: TextIO
):
    print(f'<polygon points="{x1},{y1} {x2},{y2}" style="{__LINE_STYLE}"/>', file=file)


def __write_table(
    text: str,
    X0: int | float,
    Y0: int | float,
    x: list[list[int]],
    C: list[list[int]],
    C_: list[list[int]],
    W: list[int],
    T: list[int],
    file: TextIO,
):
    r = len(W)
    c = len(T)

    w = (c + 1) * 2 * __X
    h = (r + 1) * 2 * __Y

    __write_text_in_box(text, X0, X0 + __X, Y0, Y0 + __Y, file)
    __write_text_in_box("挖方量", X0 + w - __X, X0 + w, Y0, Y0 + __Y, file)
    __write_text_in_box("填方量", X0, X0 + __X, Y0 + h - __Y, Y0 + h, file)
    __write_text_in_box(f"{sum(W)}", X0 + w - __X, X0 + w, Y0 + h - __Y, Y0 + h, file)

    __write_line(X0, X0 + w, Y0 + __Y, Y0 + __Y, file)
    __write_line(X0, X0 + w, Y0 + h, Y0 + h, file)
    for i in range(r):
        y1 = Y0 + (i * 2 + 1) * __Y
        y2 = Y0 + ((i + 1) * 2 + 1) * __Y
        __write_text_in_box(f"W{i+1}", X0, X0 + __X, y1, y2, file)
        __write_text_in_box(f"{W[i]}", X0 + w - __X, X0 + w, y1, y2, file)
        __write_line(X0, X0 + w, y2, y2, file)

    __write_line(X0 + __X, X0 + __X, Y0, Y0 + h, file)
    __write_line(X0 + w, X0 + w, Y0, Y0 + h, file)
    for j in range(c):
        x1 = X0 + (j * 2 + 1) * __X
        x2 = X0 + ((j + 1) * 2 + 1) * __X
        __write_text_in_box(f"T{j+1}", x1, x2, Y0, Y0 + __Y, file)
        __write_text_in_box(f"{T[j]}", x1, x2, Y0 + h - __Y, Y0 + h, file)
        __write_line(x2, x2, Y0, Y0 + h, file)

    for i in range(r):
        for j in range(c):
            assert x[i][j] >= 0
            x1 = X0 + (2 * j + 1) * __X
            y1 = Y0 + (2 * i + 1) * __Y
            __write_text_in_box(
                f"{x[i][j]}" if x[i][j] > 0 else f"{C[i][j]-C_[i][j]:+}",
                x1,
                x1 + __X,
                y1,
                y1 + __Y * 2,
                file,
            )
            __write_text_in_box(
                str(C[i][j]), x1 + __X, x1 + __X * 2, y1, y1 + __Y, file
            )
            __write_text_in_box(
                str(C_[i][j]), x1 + __X, x1 + __X * 2, y1 + __Y, y1 + __Y * 2, file
            )
            __write_line(x1 + __X, x1 + __X, y1, y1 + __Y * 2, file)
            __write_line(x1 + __X, x1 + __X * 2, y1 + __Y, y1 + __Y, file)


def __print_table(t: list[list[bool]]):
    print()
    for r in t:
        print(*["1" if i else "0" for i in r])


def __calcPrice(x: list[list[int]], c: list[list[int]], c_: list[list[int]]):
    I = len(x)
    J = len(x[0])
    avail: list[list[bool]] = [[False for j in range(J)] for i in range(I)]

    for i in range(0, I):
        for j in range(0, J):
            if x[i][j] > 0:
                c_[i][j] = c[i][j]
                avail[i][j] = True
    changing = True
    while changing:
        changing = False
        for i1 in range(0, I):
            for i2 in range(0, I):
                if i1 == i2:
                    continue
                assert i1 != i2
                for j1 in range(0, J):
                    for j2 in range(0, J):
                        if j1 == j2:
                            continue
                        assert j1 != j2
                        if avail[i1][j1] and avail[i2][j2]:
                            if avail[i1][j2] and not avail[i2][j1]:
                                c_[i2][j1] = c_[i1][j1] + c_[i2][j2] - c_[i1][j2]
                                avail[i2][j1] = True
                                changing = True
    assert all(all(R) for R in avail), "假想价格系数求解不完全。"
    __checkDiagonal(I, J, c_)


def __findEdge(
    i0: int,
    j0: int,
    points: list[tuple[int, int]],
    imap: dict[int, set[int]],
    jmap: dict[int, set[int]],
    horizontal_or_vertical: bool,
) -> list[tuple[int, int]] | None:
    i, j = points[len(points) - 1]
    candidate: set[int]
    if horizontal_or_vertical:
        candidate = jmap[j]
        if j == j0 and i != i0:
            return points.copy()
        for _i in candidate:
            _imap = copy.deepcopy(imap)
            _jmap = copy.deepcopy(jmap)
            _imap[_i].remove(j)
            _jmap[j].remove(_i)
            res = __findEdge(
                i0, j0, points + [(_i, j)], _imap, _jmap, not horizontal_or_vertical
            )
            if not res is None:
                return res
        return None
    else:
        candidate = imap[i]
        if i == i0 and j != j0:
            return points.copy()
        for _j in candidate:
            _imap = copy.deepcopy(imap)
            _jmap = copy.deepcopy(jmap)
            _imap[i].remove(_j)
            _jmap[_j].remove(i)
            res = __findEdge(
                i0, j0, points + [(i, _j)], _imap, _jmap, not horizontal_or_vertical
            )
            if not res is None:
                return res
        return None


def __checkDiagonal(R: int, C: int, c_: list[list[int]]):
    for i1 in range(R):
        for i2 in range(i1 + 1, R):
            for j1 in range(C):
                for j2 in range(j1 + 1, C):
                    assert c_[i1][j1] + c_[i2][j2] == c_[i1][j2] + c_[i2][j1]


def __findPath(
    x0: int, y0: int, x: list[list[int]], r: int, c: int
) -> list[tuple[int, int]] | None:
    imap: dict[int, set[int]] = {}
    jmap: dict[int, set[int]] = {}
    for i in range(r):
        for j in range(c):
            if x[i][j] > 0:
                imap.setdefault(i, set())
                jmap.setdefault(j, set())
                imap[i].add(j)
                jmap[j].add(i)
    res = __findEdge(x0, y0, [(x0, y0)], imap, jmap, True)
    return res


def __manipulateTable(
    x: list[list[int]], c: list[list[int]], c_: list[list[int]]
) -> bool:
    i_min: int | None = None
    j_min: int | None = None
    _min: int | None = None
    R = len(x)
    C = len(x[0])
    for i in range(R):
        for j in range(C):
            if _min is None or c[i][j] - c_[i][j] < _min:
                i_min = i
                j_min = j
                _min = c[i][j] - c_[i][j]
    if i_min is None or j_min is None or _min is None:  # Completed
        return True
    if _min >= 0:
        return True
    points: list[tuple[int, int]] = []
    points.append((i_min, j_min))

    i0, j0 = points[len(points) - 1]
    l = __findPath(i0, j0, x, R, C)
    assert not l is None, "路径查找失败"
    min_x = None
    assert len(l) % 2 == 0

    L = list(zip(islice(l, 0, len(l), 2), islice(l, 1, len(l), 2), strict=True))
    for (i1, j1), (i2, j2) in L:
        if min_x is None or min_x > x[i2][j2]:
            min_x = x[i2][j2]
    assert not min_x is None
    for (i1, j1), (i2, j2) in L:
        x[i1][j1] += min_x
        x[i2][j2] -= min_x
    return False


def __svg_head(r: int, c: int, file: TextIO):
    print(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{(c+1)*2*__X}" height="{(r+1)*2*__Y}" version="1.1">'
        + """<style>
@media (prefers-color-scheme: dark){
    *{
        background-color:black;    
        stroke:white;
    }
}
</style>""",
        file=file,
    )


def __svg_tail(file: TextIO):
    print(
        "</svg>",
        file=file,
    )


def __initialTable(
    *,
    x: list[list[int]],
    costs: list[list[int]],
    c_: list[list[int]],
    W: list[int],
    T: list[int],
    r: int,
    c: int,
    p: str,
):
    with open(p, "w", encoding="UTF-8") as file:
        __svg_head(r, c, file)

        w = W.copy()
        t = T.copy()
        while True:
            initialized = False
            i_min = 0
            j_min = 0
            _min = costs[0][0]
            for i in range(0, r):
                for j in range(0, c):
                    if x[i][j] > 0:
                        continue
                    if w[i] == 0 or t[j] == 0:
                        continue
                    if not initialized or costs[i][j] < _min:
                        _min = costs[i][j]
                        i_min = i
                        j_min = j
                        initialized = True
            if not initialized:
                break
            _x = min(w[i_min], t[j_min])
            x[i_min][j_min] = _x
            w[i_min] -= _x
            t[j_min] -= _x

            if max(w) == 0 and max(t) == 0:
                break

        __calcPrice(x, costs, c_)
        __write_table(f"初始方案", 0, 0, x, costs, c_, W, T, file)
        __svg_tail(file=file)

        total = 0
        for i in range(r):
            for j in range(c):
                if x[i][j] > 0:
                    total += x[i][j] * costs[i][j]
        print(f"Z0 = {total}")


def tableManipulationMethod(
    costs: list[list[int]],
    W: list[int],
    T: list[int],
    path: Callable[[int], str],
):
    r = len(W)
    c = len(T)

    x: list[list[int]] = [[0 for j in range(c)] for i in range(r)]
    c_: list[list[int]] = [[0 for j in range(c)] for i in range(r)]

    assert sum(W) == sum(T), "请保证填挖平衡。"

    __initialTable(x=x, costs=costs, c_=c_, W=W, T=T, r=r, c=c, p=path(0))

    times: int = 1

    completed = False
    while not completed:
        if __manipulateTable(x, costs, c_):
            break
        __calcPrice(x, costs, c_)
        with open(path(times), "w", encoding="UTF-8") as file:
            __svg_head(r, c, file)
            __write_table(f"第{times}次调整", 0, 0, x, costs, c_, W, T, file)
            __svg_tail(file)

            total = 0
            for i in range(r):
                for j in range(c):
                    if x[i][j] > 0:
                        total += x[i][j] * costs[i][j]
            print(f"Z{times} = {total}")
        times += 1
