from ..main import *


def Q1():
    Ec = 2.51e4
    Es = 1.97e5
    alpha_E = Es / Ec
    As = 1472
    h = 600
    b = 250
    ft = 2.6
    fc = 23
    h0 = h - 25 - 25 / 2

    _xcr = xcr(alpha_E, As, b, h)
    _Mcr = Mcr(ft, b, h, _xcr, alpha_E, As, h0)

    sigma_s = 2 * alpha_E * ft
    signa_c_t = (ft * b * (h - _xcr) + sigma_s * As) / 0.5 / b / _xcr
    phi_cr = ft / 0.5 / Ec / (h - _xcr)
    print(_Mcr, sigma_s, signa_c_t, phi_cr)


def Q2():
    Ec = 2.51e4
    Es = 1.97e5
    alpha_E = Es / Ec
    As = 1472
    h = 600
    b = 250
    fy = 357
    ft = 2.6
    fc = 23
    h0 = h - 25 - 25 / 2

    _rho = rho(As, b * h)

    _xi_n = xi_n_low_fit(_rho, fy, fc)
    _Mu = Mu_low_fit(fy, As, h0, _xi_n)
    phi_u = fy / Es / (h - _xi_n)
    _alpha_1 = alpha_1_low()
    _xi = xi(_rho, fy, _alpha_1, fc)
    _Mu_simplified = Mu_fit_simplified(_alpha_1, fc, b, h, _xi)
    print(_Mu, phi_u, _Mu_simplified)


def Q3():
    Ec = 2.51e4
    Es = 1.97e5
    alpha_E = Es / Ec
    h = 600
    b = 250
    fy = 357
    ft = 2.6
    fc = 23
    h0 = h - 25 - 25 / 2
    epsilon_cu = 0.0033

    if 1:
        As = 2 * pi * 12 ** 2 / 4

        _Mu_simplified = Mu(b, h, As, fc, ft, fy, Es, Ec, epsilon_cu, h0)
        print(_Mu_simplified)

    if 2:
        As = 10 * pi * 28 ** 2 / 4

        _Mu_simplified = Mu(b, h, As, fc, ft, fy, Es, Ec, epsilon_cu, h0)
        print(_Mu_simplified)


def Q4():
    Ec = 2.51e4
    epsilon_cu = 0.0033

    Es = 2.0e5
    h = 90
    b = 200
    fy = 280
    ft = 1.6
    fc = 11.9
    h0 = h - 25 - 10 / 2

    As = 2 * pi * 10 ** 2 / 4

    _Mu_simplified = Mu(b, h, As, fc, ft, fy, Es, Ec, epsilon_cu, h0)
    print(_Mu_simplified)


def Q5():
    Ec = 2.51e4
    epsilon_cu = 0.0033

    Es = 1.97e5
    h = 500
    b = 220
    fy = 365
    ft = 1.2
    fc = 13
    h0 = h - 25 - 25 - (25 + 20) / 2

    As = 2 * pi * (22 ** 2 + 20 ** 2) / 4

    _Mu_simplified = Mu(b, h, As, fc, ft, fy, Es, Ec, epsilon_cu, h0)
    print(_Mu_simplified)


def Q6():
    Ec = 2.51e4
    epsilon_cu = 0.0033

    Es = 1.97e5
    h = 500
    b = 200
    fy = 310
    ft = 1.2
    fc = 13
    h0 = h - 35

    listAs = [
        design(b, h, h0, fc, ft, fy, M)
        for M in [40e6, 60e6, 80e6, 100e6, 120e6, 140e6, 160e6, 180e6, 200e6, 220e6]
    ]
    print(listAs)


def Q7():
    h = 80
    b = 1000
    fy = 270
    ft = 1.2
    fc = 13
    h0 = h - 35
    M = 4 * 1.92e3 ** 2 / 8

    As = design(b, h, h0, fc, ft, fy, M)
    print(As)


def Q8():
    b = 400
    h = 1200
    As_ = 4 * pi * 28 ** 2 / 4
    As = 12 * pi * 28 ** 2 / 4
    fc = 14.3
    ft = 1.43
    Ec = 3e4
    fy = 310
    Es = 1.97e5
    alpha_E = Es / Ec
    As2 = As_
    As1 = As - As2
    _as = 35
    _as_ = 35
    h0 = h - _as
    _rho = rho(As1, b * h)
    _xi = xi(_rho, fy, alpha_1_low(), fc)
    _Mcr = Mcr_simplified(alpha_E)
    Mu_ = fy * As_ * (h0 - _as_)
