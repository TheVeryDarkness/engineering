from functools import reduce
from itertools import repeat
from math import ceil, floor, gcd
from typing import Generator, TextIO
import roman


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
__CIRCLE_PROP = f'style="fill: none; stroke: black;"'
__EXTRA_Y_OFFSET = 2


def __add_append(l: list[int], i: int):
    l.append((l[len(l) - 1] if len(l) > 0 else 0) + i)
    return l


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
    time_cost: list[list[int]],
    m: int,
    data: list[list[list[tuple[int, int]]]],
    file: TextIO,
    vertical: bool,
    draw_dash: bool = False,
):
    """
    data: processes * crews -> section, start time
    """
    n = len(data)
    if vertical:
        for i_proc, proc in enumerate(data):
            for i_crew, sec_per_crew in enumerate(proc):
                for i_sec, t in sec_per_crew:
                    length = time_cost[i_proc][i_sec]

                    CREW_NAME = f"{roman.toRoman(i_proc+1)}-{i_crew+1}"
                    CREW_NAME_WIDTH = len(CREW_NAME) * __FONT_SIZE + __MARGIN
                    X1 = X0 + t * __X
                    X2 = X0 + (t + length) * __X
                    Y1 = Y0 + (m - i_sec) * __Y
                    Y2 = Y0 + (m - i_sec - 1) * __Y
                    file.write(
                        f"""
                        <polyline points="{X1},{Y1} {X2},{Y2}" style="{__LINE_STYLE}"/>
                        <text x="{X1+__X/2}" y="{Y1-__X/2/length}" {__LEFT_TEXT_PROP}>{CREW_NAME}</text>
                        """
                    )
        if draw_dash:
            for i_proc, proc in enumerate(data):
                if i_proc == 0:
                    continue
                for i_crew, sec_per_crew in enumerate(proc):
                    for i_sec, t in reversed(sec_per_crew):
                        length = time_cost[i_proc][i_sec]
                        if i_sec + 1 == m:
                            continue
                        PREV = data[i_proc - 1][i_crew][i_sec + 1][1]
                        assert i_sec + 1 == m or PREV <= t
                        X1 = X0 + t * __X
                        X2 = X0 + (t + length) * __X
                        Y1 = Y0 + (m - i_sec) * __Y
                        Y2 = Y0 + (m - i_sec - 1) * __Y
                        file.write(
                            f"""
                            <polyline points="{X1},{Y1-__Y} {X2},{Y2-__Y}" style="{__LINE_STYLE}" stroke-dasharray="2 3"/>
                            """
                        )
                        if PREV == t:
                            break
            for i_proc, proc in enumerate(data):
                if i_proc + 1 == n:
                    continue
                for i_crew, sec_per_crew in enumerate(proc):
                    for i_sec, t in sec_per_crew:
                        length = time_cost[i_proc][i_sec]
                        if i_sec == 0:
                            continue
                        NEXT = data[i_proc + 1][i_crew][i_sec - 1][1]
                        assert i_sec + 1 == m or t <= NEXT
                        if NEXT == t:
                            break
                        X1 = X0 + t * __X
                        X2 = X0 + (t + length) * __X
                        Y1 = Y0 + (m - i_sec) * __Y
                        Y2 = Y0 + (m - i_sec - 1) * __Y
                        file.write(
                            f"""
                            <polyline points="{X1},{Y1+__Y} {X2},{Y2+__Y}" style="{__LINE_STYLE}" stroke-dasharray="2 3"/>
                            """
                        )

    else:
        y = 3
        for i_proc, proc in enumerate(data):
            for i_crew, sec_per_crew in enumerate(proc):
                for i_sec_of_crew, (i_sec, t) in enumerate(sec_per_crew):
                    length = time_cost[i_proc][i_sec]

                    CREW_NAME = f"{roman.toRoman(i_proc+1)}-{i_crew+1}"
                    CREW_NAME_WIDTH = len(CREW_NAME) * __FONT_SIZE + __MARGIN

                    Y_OFFSET = -__Y / 2 + (
                        __OFFSET if i_sec_of_crew % 2 == 0 else -__OFFSET
                    )

                    # 施工过程
                    file.write(
                        f"""
<polyline points="{__X*(2+t)},{y*__Y+Y_OFFSET} {__X*(2+t+length)},{y*__Y+Y_OFFSET}" style="{__LINE_STYLE}"/>
                    """
                    )
                    MX = __X * (2 + t + length / 2) - (
                        (0.7 * __FONT_SIZE) if length % 2 == 0 else 0
                    )
                    __write_circled_text(i_sec + 1, MX, y * __Y + Y_OFFSET, file)
                y += 1


def __write_chart(
    *,
    time_cost: list[int] | list[list[int]],
    UNIT: str,
    m: int,
    data: list[list[list[tuple[int, int]]]],
    names: list[str],
    file: TextIO,
    vertical: bool,
    K: int,
    draw_dash: bool = False,
):
    """
    data: process * crew -> section, start time
    time_cost: process | process * section
    """
    expanded_costs: list[list[int]] = []
    for proc in time_cost:
        if isinstance(proc, int):
            l: list[int] = list(repeat(proc, m))
            expanded_costs.append(l)
        else:
            expanded_costs.append(proc)
    Tp_K = max(
        max(
            max(start + (expanded_costs[i_proc][i_sec]) for i_sec, start in crew)
            for crew in proc
        )
        for i_proc, proc in enumerate(data)
    )
    _N = sum(len(processes) for processes in data)
    if vertical:  # 垂直图表
        W = Tp_K + 1
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
                __write_circled_text(
                    str(m + 3 - i), __X / 2, (i - 0.5) * __Y + __FONT_SIZE / 2, file
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
            time_cost=expanded_costs,
            m=m,
            data=data,
            file=file,
            vertical=vertical,
            draw_dash=draw_dash,
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
        W = Tp_K + 2
        H = _N + 2
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
        __write_multiline_text("施工过程", __X * 0.5, __Y, __X, __Y * 2, file)
        __write_multiline_text("施工队", __X * 1.5, __Y, __X, __Y * 2, file)
        file.write("<!--Horizontal lines-->")

        # 表头分隔线
        file.write(
            f"""
<polyline points="{__X*2},{__Y} {WIDTH},{__Y}" style="{__LINE_STYLE}"/>
<polyline points="{0},{__Y*2} {WIDTH},{__Y*2}" style="{__LINE_STYLE}"/>
        """
        )
        i = 0
        for (i_process, crews) in enumerate(data):
            Ni = len(crews)
            y = i + 2
            # 施工段分隔线
            file.write(
                f'<polyline points="0,{(y+Ni)*__Y} {__X*2},{(y+Ni)*__Y}" style="{__LINE_STYLE}"/>'
            )
            for i_crew in range(0, Ni):
                _y = y + i_crew
                # 施工队分隔线
                file.write(
                    f"""
<polyline points="{__X*1},{_y*__Y} {WIDTH},{_y*__Y}" style="{__LINE_STYLE}"/>
                """
                )
                # 施工队名称
                file.write(
                    f'<text x="{(3/2)*__X}" y="{(_y+1)*__Y-__MARGIN}" {__MIDDLE_TEXT_PROP}>{roman.toRoman(i_process+1)}-{i_crew+1}</text>'
                )
            if i_process < len(names):
                NAME = names[i_process]
                __write_multiline_text(
                    NAME, __X / 2, (y + Ni / 2) * __Y, __X, Ni * __Y, file
                )
            else:
                NAME = roman.toRoman(i_process + 1)
                __write_text(NAME, __X / 2, (y + Ni / 2) * __Y, file)
            i += Ni
        i = None

        file.write("<!--Vertical lines-->")
        # 竖线
        file.write(
            f'\n<polyline points="{1*__X},{0} {1*__X},{HEIGHT}" style="{__LINE_STYLE}"/>'
            f'\n<polyline points="{2*__X},{0} {2*__X},{HEIGHT}" style="{__LINE_STYLE}"/>'
        )
        for i in range(3, W):
            file.write(
                f'\n<polyline points="{i*__X},{__Y} {i*__X},{HEIGHT}" style="{__LINE_STYLE}"/>'
            )

        file.write("<!--Process-->")
        __write_process_lines(
            __X * 2,
            __Y * 2,
            time_cost=expanded_costs,
            m=m,
            data=data,
            file=file,
            vertical=vertical,
        )

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


def __write_text(
    TEXT: str,
    X: int | float,
    Y: int | float,
    file: TextIO,
):
    file.write(
        f'<text x="{X}" y="{Y-__EXTRA_Y_OFFSET}" {__MIDDLE_TEXT_PROP}>{TEXT}</text>'
    )


def __write_multiline_text(
    TEXT: str,
    X: int | float,
    Y: int | float,
    W: int,
    H: int,
    file: TextIO,
):
    C_R = floor((W - __MARGIN * 2) / __FONT_SIZE)
    ROWS = ceil(len(TEXT) / C_R)
    CONTAINABLE_ROWS = ceil(H / __FONT_SIZE)
    if ROWS > CONTAINABLE_ROWS:
        print("Text too long.")
    for i_r in range(0, ROWS):
        S = TEXT[i_r * C_R : (i_r + 1) * C_R]
        file.write(
            f'<text textLength="{__FONT_SIZE*len(S)}" x="{X}" y="{Y+(i_r-ROWS/2+1)*__FONT_SIZE-__EXTRA_Y_OFFSET}" {__MIDDLE_TEXT_PROP}>{S}</text>'
        )


def __write_circled_text(
    TEXT: str | int | float, X: int | float, Y: int | float, file: TextIO
):
    file.write(
        f"""
    <text x="{X}" y="{Y-__EXTRA_Y_OFFSET}" {__MIDDLE_TEXT_PROP}>{TEXT}</text>
    <circle cx="{X}" cy="{Y-__FONT_SIZE/2}" r="{__FONT_SIZE/2}" {__CIRCLE_PROP}/>
    """
    )


def normal_beat_flow(
    section: int,
    names: list[str],
    time_costs: list[int],
    UNIT: str,
    file: TextIO,
    vertical: bool = False,
    K: int = 1,
    Z1: list[int] = [],
    Z2: list[int] = [],
    Z3: list[int] = [],
):

    n = len(time_costs)  # 施工过程数
    m = section  # 施工段数
    K0 = K
    K = K0 * gcd(*time_costs)
    Ns = [1 for _ in time_costs]
    N = n
    time = [t // K for t in time_costs]

    Tp = (m * time[0]) * K
    for i in range(1, n):
        Tp += max(time[i] * m - time[i - 1] * (m - 1), time[i]) * K

    START = [0]  # Start time of each process
    for i_proc, Ni in enumerate(Ns):  # Index of previous process
        if i_proc + 1 == n:
            break
        assert i_proc + 1 == len(START)
        START_i = START[i_proc] + time[i_proc]
        if i_proc + 1 < n:
            END = START[i_proc] + m * time[i_proc]
            START_i = max(START_i, END - (m - 1) * time[i_proc + 1])
        START.append(START_i)
    print(
        f"""
施工段数目  m = {m}
流水节拍    K = {K}
各班组数量 Ni = {Ns}
班组总数    N = {N}
计划工期   Tp = {Tp}
"""
    )
    __write_chart(
        m=m,
        time_cost=time,
        UNIT=UNIT,
        names=names,
        K=K,
        data=[
            [
                __collect_not_none(
                    (
                        (i_sec, START[i_proc] + i_sec * time[i_proc])
                        for i_sec in range(m)
                    )
                )
            ]
            for i_proc in range(n)
        ],
        file=file,
        vertical=vertical,
    )


def accelerated_beat_flow(
    section: int,
    names: list[str],
    time_costs: list[int],
    UNIT: str,
    file: TextIO,
    vertical: bool = False,
    K: int = 1,
    Z1: list[int] = [],
    Z2: list[int] = [],
    Z3: list[int] = [],
):

    n = len(time_costs)  # 施工过程数
    m = section  # 施工段数
    K0 = K
    K = gcd(*time_costs) * K0
    Ns = [Ki // K for Ki in time_costs]  # 理论
    Ts = [min(Ki // K, m) for Ki in time_costs]  # 实际
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
    __write_chart(
        m=m,
        time_cost=Ns,
        UNIT=UNIT,
        names=names,
        K=K,
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


def non_beat_flow(
    section: int,
    names: list[str],
    time_costs: list[list[int]],
    UNIT: str,
    svg: TextIO,
    vertical: bool = False,
    K: int = 1,
    Z1: list[int] = [],
    Z2: list[int] = [],
    Z3: list[int] = [],
):
    """
    time_costs: processes * sections
    """
    n = len(time_costs)  # 施工过程数
    m = section  # 施工段数
    K0 = K

    time_continue: list[list[int]] = [
        reduce(__add_append, time_cost, [0]) for time_cost in time_costs
    ]

    print("施工过程已持续总时间：")
    for proc in time_continue:
        print(proc)
    B: list[int] = []
    print("施工过程时间间距：")
    for i_proc, proc in enumerate(time_continue):
        diff: list[int] = []
        if i_proc + 1 >= len(time_continue):
            break
        for i_sec, t in enumerate(proc):
            last = time_continue[i_proc + 1][i_sec - 1] if i_sec > 0 else 0
            diff.append(t - last)
        B.append(max(diff))
        print(diff)
    print("流水步距：")
    print(B)
    process_start: list[int] = reduce(__add_append, B, [0])

    print(
        f"""
施工段数目 m = {m}
流水节拍   K = {K}
"""
    )
    __write_chart(
        m=m,
        time_cost=time_costs,
        UNIT=UNIT,
        names=names,
        K=K,
        data=[
            [
                __collect_not_none(
                    (
                        (i_sec, time_continue[i_proc][i_sec] + process_start[i_proc])
                        for i_sec in range(m)
                    )
                )
            ]
            for i_proc in range(n)
        ],
        file=svg,
        vertical=vertical,
        draw_dash=vertical,
    )
