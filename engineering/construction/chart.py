from math import ceil, floor, gcd
from types import NoneType
from typing import Generator, TextIO, TypeVar


__X = 80
__Y = 60
__FONT_SIZE = 20
__MARGIN = 15
__OFFSET = 8
__LINE_STYLE = "stroke:rgb(0,0,0);stroke-width:2;fill:none;"
__TEXT_PROP = f'font-size="{__FONT_SIZE}"'
__MIDDLE_TEXT_PROP = f'text-anchor="middle" {__TEXT_PROP}'
__RIGHT_TEXT_PROP = f'text-anchor="start" {__TEXT_PROP}'
__LEFT_TEXT_PROP = f'text-anchor="end" {__TEXT_PROP}'
__VERTICAL_TEXT_PROP = f'style="writing-mode: tb; glyph-orientation-vertical: 0; text-orientation: upright;"'


def __collect_not_none(
    l: Generator[tuple[int, int] | None, None, None]
) -> list[tuple[int, int]]:
    res: list[tuple[int, int]] = []

    try:
        while True:
            item = next(l)
            if not (item is None):
                res.append(item)
    except StopIteration as e:
        return res


def __write_process_lines(
    X0: int | float,
    Y0: int | float,
    time_cost: list[int],
    m: int,
    data: list[list[list[tuple[int, int]]]],
    file: TextIO,
    vertical: bool,
):
    """
    data: processes * crews -> section, start time
    """
    print(data)
    for i_proc, proc in enumerate(data):
        for i_crew, proc_per_crew in enumerate(proc):
            for i_sec, t in proc_per_crew:
                length = time_cost[i_proc]

                CREW_NAME = f"{i_crew+1}-{i_crew}"
                CREW_NAME_WIDTH = len(CREW_NAME) * __FONT_SIZE + __MARGIN
                X1 = X0 + t * __X
                X2 = X0 + (t + length) * __X
                Y1 = Y0 + (m - i_sec) * __Y
                Y2 = Y0 + (m - i_sec - 1) * __Y
                file.write(
                    f"""'
                    <polyline points="{X1},{Y1} {X2},{Y2}" style="{__LINE_STYLE}"/>
                    <text x="{X1+__X/2}" y="{Y1-__X/2/length}" {__LEFT_TEXT_PROP}>{CREW_NAME}</text>
                    """
                )


def __write_multiline_text(
    TEXT: str, X: int | float, Y: int | float, W: int, H: int, file: TextIO
):
    C_R = floor((W - __MARGIN * 2) / __FONT_SIZE)
    ROWS = ceil(len(TEXT) / C_R)
    CONTAINABLE_ROWS = ceil(H / __FONT_SIZE)
    for i_r in range(0, ROWS):
        S = TEXT[i_r * C_R : (i_r + 1) * C_R]
        # 施工段名称（分行）
        file.write(
            f'<text textLength="{__FONT_SIZE*len(S)}" x="{X}" y="{Y+(i_r-ROWS/2+1)*__FONT_SIZE}" {__MIDDLE_TEXT_PROP}>{S}</text>'
        )


def accelerated_beat_flow(
    section: int,
    names: list[str],
    time_costs: list[int],
    UNIT: str,
    file: TextIO,
    vertical: bool = False,
    hideUnused: bool = True,
):
    n = len(time_costs)  # 施工过程数
    m = section  # 施工段数
    K = gcd(*time_costs)
    Ns = [Ki // K for Ki in time_costs]
    Ts = [min(Ki // K, m) for Ki in time_costs]
    Hs = Ts if hideUnused else Ns
    _N = sum(Ns)
    N = sum(Ts)
    Tp = (m + _N - 1) * K
    START = [0]  # Start time of each process
    for Ni in Ns:
        START.append(START[len(START) - 1] + Ni)
    print(
        f"""
施工段数目  m = {m}
流水节拍    K = {K}
各班组数量 Ni = {Ts}
班组总数    N = {N}
计划工期   Tp = {Tp}
"""
    )

    if vertical:  # 垂直图表
        W = m + _N - 1 + 1
        H = m + 2
        WIDTH = W * __X
        HEIGHT = H * __Y
        file.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" version="1.1">'
        )

        # 文字
        file.write(
            f"""
<!--Description-->
<text x="{((1+W)/2)*__X}" y="{__Y-__MARGIN}" {__MIDDLE_TEXT_PROP}>施工进度/{UNIT}</text>
            """
        )
        __write_multiline_text("施工段", __X / 2, __Y, __X, __Y * 2, file)
        file.write("<!--Horizontal lines-->")
        # 横线
        file.write(
            f"""
<polyline points="{__X*1},{__Y} {WIDTH},{__Y}" style="{__LINE_STYLE}"/>
    """
        )
        for i in range(2, m + 3):
            # 横线
            file.write(
                f"""
<polyline points="{0},{i*__Y} {WIDTH},{i*__Y}" style="{__LINE_STYLE}"/>
    """
            )
            if i != 2:
                __write_multiline_text(
                    str(m + 3 - i), __X / 2, (i - 0.5) * __Y, __X, __Y, file
                )

        file.write("<!--Vertical lines-->")
        # Vertical
        file.write(
            f'\n<polyline points="{__X},{0} {__X},{HEIGHT}" style="{__LINE_STYLE}"/>'
        )
        for i in range(2, W):
            file.write(
                f'\n<polyline points="{i*__X},{__Y} {i*__X},{HEIGHT}" style="{__LINE_STYLE}"/>'
            )

        file.write("<!--Process-->")
        __write_process_lines(
            __X,
            __Y * 2,
            Ns,
            m,
            data=[
                [
                    __collect_not_none(
                        (
                            (i_sec, START[i_proc] + i_sec)
                            if i_crew == i_sec % Ts[i_proc]
                            else None
                            for i_sec in range(m)
                        )
                    )
                    for i_crew in range(Ts[i_proc])
                ]
                for i_proc in range(n)
            ],
            file=file,
            vertical=vertical,
        )

        file.write("<!--Time-->")
        for t in range(1, W):
            file.write(
                f'\n<text x="{t*__X+__X/2}" y="{__Y*2-__MARGIN}" {__MIDDLE_TEXT_PROP}>{t*K}</text>'
            )

        file.write("<!--Border-->")
        file.write(
            f'\n<polyline points="{WIDTH},{HEIGHT} {WIDTH},0" style="{__LINE_STYLE}"/>'
        )
    else:  # 水平图表
        W = m + _N - 1 + 2
        H = sum(Hs) + 2
        WIDTH = W * __X
        HEIGHT = H * __Y
        file.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" version="1.1">'
        )

        # 文字
        file.write(
            f"""
<!--Description-->
<text x="{((2+W)/2)*__X}" y="{__Y-__MARGIN}" {__MIDDLE_TEXT_PROP}>施工进度/{UNIT}</text>
            """
        )
        __write_multiline_text("施工段", __X * 0.5, __Y, __X, __Y * 2, file)
        __write_multiline_text("施工队", __X * 1.5, __Y, __X, __Y * 2, file)
        file.write("<!--Horizontal lines-->")

        i_section = 0
        j = -2
        for i in range(1, H + 1):
            TI = Ts[i_section]
            NI = Ns[i_section]
            HI = Hs[i_section]

            # 横线
            file.write(
                f"""
<polyline points="{__X*1 if i not in[1,2] else 0 if i in [2] else __X*2},{i*__Y} {WIDTH},{i*__Y}" style="{__LINE_STYLE}"/>
            """
            )
            if j >= 0:
                if j < TI:
                    # 施工队名称
                    file.write(
                        f'<text x="{(3/2)*__X}" y="{i*__Y-__MARGIN}" {__MIDDLE_TEXT_PROP}>{i_section}-{j}</text>'
                    )
                for _j in range(0, K):
                    Y_OFFSET = -__Y / 2 + (__OFFSET if _j % 2 == 0 else -__OFFSET)
                    BEGIN = START[i_section]
                    if _j * TI + j >= m:
                        break
                    # 施工过程
                    file.write(
                        f"""
<polyline points="{__X*(2+j+BEGIN+_j*NI)},{i*__Y+Y_OFFSET} {__X*(2+j+BEGIN+(_j+1)*NI)},{i*__Y+Y_OFFSET}" style="{__LINE_STYLE}"/>
                    """
                    )

            j += 1
            if j == HI:
                i_section += 1
                j = 0

        file.write("<!--Vertical lines-->")
        for i in range(1, W):
            # 竖线
            file.write(
                f'\n<polyline points="{i*__X},{__Y if i not in [1,2] else 0} {i*__X},{HEIGHT}" style="{__LINE_STYLE}"/>'
            )

        file.write("<!--Horizontal lines between sections-->")
        y = 2
        for i, Ni in enumerate(Hs):
            # 施工段分隔线
            file.write(
                f'<polyline points="0,{(y+Ni)*__Y} {__X*2},{(y+Ni)*__Y}" style="{__LINE_STYLE}"/>'
            )
            NAME = names[i] if i < len(names) else str(i)
            __write_multiline_text(
                NAME, __X / 2, (y + Ni / 2) * __Y, __X, Ni * __Y, file
            )
            y += Ni

        file.write("<!--Time-->")
        for t in range(2, W):
            # 时间
            file.write(
                f'\n<text x="{t*__X+__X/2}" y="{__Y*2-__MARGIN}" {__MIDDLE_TEXT_PROP}>{(t-1)*K}</text>'
            )

        file.write("<!--Border-->")
        # 图表右边界
        file.write(
            f'\n<polyline points="{WIDTH},{HEIGHT} {WIDTH},0" style="{__LINE_STYLE}"/>'
        )

    file.write("<!--End-->")
    file.write("\n</svg>")
