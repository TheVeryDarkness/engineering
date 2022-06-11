from cmath import pi
from math import inf, sin


def Vc(ft, b, h0):
    return 0.7 * ft * b * h0


def Vumax(hw_b, beta_c, fc, b, h0):
    a = 0.25 if hw_b >= 6 else 0.2 if hw_b <= 4 else 0.35 - 0.025 * hw_b
    return a * beta_c * fc * b * h0


def Asv_s(V, Vc, fyv, h0):
    return (V - Vc) / fyv / h0


def rho_sv(hw, beta_c, ft, fc, b, h0, V, fyv):
    _Vc = Vc(ft, b, h0)
    print(f"Vc = {_Vc}")
    if V <= _Vc:
        print("剪力较小。")
        return 0
    _Vumax = Vumax(hw / b, beta_c, fc, b, h0)
    print(f"Vumax = {_Vumax}")
    if V > _Vumax:
        print("配筋失败")
    _Asv_s = Asv_s(V, _Vc, fyv, h0)
    print(f"Asv/s = {_Asv_s}")
    return _Asv_s / b


def Vb(fy, Asb, alpha):
    return 0.8 * fy * Asb * sin(alpha)


def rho_sv_b(hw, beta_c, ft, fc, b, h0, V, fyv, fy, Asb, alpha):
    _Vc = Vc(ft, b, h0)
    print(f"Vc = {_Vc}")
    if V <= _Vc:
        print("剪力较小。")
        return 0
    _Vumax = Vumax(hw / b, beta_c, fc, b, h0)
    print(f"Vumax = {_Vumax}")
    if V > _Vumax:
        print("配筋失败")
    _Vb = Vb(fy, Asb, alpha)
    print(f"Vb = {Vb}")
    _Asv_s = Asv_s(V, _Vc + _Vb, fyv, h0)
    print(f"Asc/s = {_Asv_s}")
    return _Asv_s / b


def rho_sv_min(ft, fyv):
    return 0.24 * ft / fyv


def smax(h: float | int, _: bool):
    if h <= 150:
        return None
    elif h <= 300:
        return 150 if _ else 200
    elif h <= 500:
        return 200 if _ else 300
    elif h <= 800:
        return 250 if _ else 350
    else:
        return 300 if _ else 400


def _7_1():
    b = 200
    h = 500
    a_s = 35
    fc = 9.6
    ft = 1.1
    V = 1.2e5
    fyv = 270

    hw = h0 = h - a_s
    rho = rho_sv(hw, 1, ft, fc, b, h0, V, fyv)
    print(rho)
    rho_min = rho_sv_min(ft, fyv)
    print(rho_min)
    if rho < rho_min:
        print("配筋过少")
        rho = rho_min

    Asv_s = rho * b
    _smax = smax(h, V > Vc(ft, b, h0))
    dmin = 8 if h > 800 else 6
    As1_dmin = pi / 4 * dmin ** 2
    return


def _7_2():
    b = 200
    h = 500
    a_s = 35
    fc = 9.6
    ft = 1.1
    V = 2.8e5
    fyv = 270

    hw = h0 = h - a_s
    rho = rho_sv(hw, 1, ft, fc, b, h0, V, fyv)
    print(rho)
    rho_min = rho_sv_min(ft, fyv)
    print(rho_min)
    if rho < rho_min:
        print("配筋过少")
        rho = rho_min

    Asv_s = rho * b
    _smax = smax(h, V > Vc(ft, b, h0))
    dmin = 8 if h > 800 else 6
    As1_dmin = pi / 4 * dmin ** 2
    return


def _7_3():
    b = 200
    h = 400
    a_s = 35
    fc = 9.6
    ft = 1.1
    fyv = 270

    hw = h0 = h - a_s

    N = 40e3 * 6.3
    N2 = 6.3 / 2 * 40e3 * 6.3 / 4.5
    N1 = N - N2

    for V in [N1, 1.8 * 40e3, N2 - 1.8 * 40e3]:
        print(f"V = {V}")
        rho = rho_sv(hw, 1, ft, fc, b, h0, V, fyv)
        print(rho)
        rho_min = rho_sv_min(ft, fyv)
        print(rho_min)
        if rho < rho_min:
            print("配筋过少")
            rho = rho_min

        Asv_s = rho * b
        _smax = smax(h, V > Vc(ft, b, h0))
        dmin = 8 if h > 800 else 6
        As1_dmin = pi / 4 * dmin ** 2
        print(Asv_s)


def _7_4():
    b = 250
    h = 600
    a_s = 25 + 25 / 2
    fc = 9.6
    ft = 1.1
    fyv = 270

    hw = h0 = h - a_s

    V = 201.6e3

    print(f"V = {V}")
    rho = rho_sv(hw, 1, ft, fc, b, h0, V, fyv)
    print(rho)
    rho_min = rho_sv_min(ft, fyv)
    print(rho_min)
    if rho < rho_min:
        print("配筋过少")
        rho = rho_min

    Asv_s = rho * b
    _smax = smax(h, V > Vc(ft, b, h0))
    dmin = 8 if h > 800 else 6
    As1_dmin = pi / 4 * dmin ** 2
    print(Asv_s)


if __name__ == "__main__":
    if 0:
        _7_1()
    if 0:
        _7_2()
    if 0:
        _7_3()
    if 1:
        _7_4()
