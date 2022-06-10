from math import pi
from math import sqrt
from this import d


def rho(As, bh):
    return As / bh if As < bh * 0.03 else As / (bh - As)


def xcr(alpha_E, As, b, h):
    return (1 + 2 * alpha_E * As / b / h) / (1 + alpha_E * As / b / h) * h / 2


def Mcr(ft, b, h, xcr, alpha_E, As, h0):
    return ft * b * (h - xcr) * (
        (h - xcr) / 2 + 2 * xcr / 3
    ) + 2 * alpha_E * ft * As * (h0 - xcr / 3)


def Mu_under_C50(sigma_s, As, h0, xi_n):
    return sigma_s * As * h0 * (1 - 0.412 * xi_n)


def xi_n_low_fit(rho, fy, fc):
    return 1.253 * rho * fy / fc


def Mu_low_fit(fy, As, h0, xi_n):
    return fy * As * h0 * (1 - 0.412 * xi_n)


def alpha_1_low():
    return 1


def beta_1_under_C50():
    return 0.8


def Mu_fit_simplified(alpha_1, fc, b, h0, xi):
    return alpha_1 * fc * b * h0 ** 2 * xi * (1 - 0.5 * xi)


def sigma_s_over_simplified(fy, xi, xi_b):
    return fy * (xi - 0.8) / (xi_b - 0.8)


def Mu_over_simplified(fy, xi, xi_b, As, alpha_1, fc, b, h0):
    sigma_s = sigma_s_over_simplified(fy, xi, xi_b)
    x = sigma_s * As / alpha_1 / fc / b
    return sigma_s * As * (h0 - x / 2)


def xi(rho, fy, alpha_1, fc):
    return rho * fy / alpha_1 / fc


def xi_b(beta_1, fy, Es, epsilon_cu):
    return beta_1 / (1 + fy / Es / epsilon_cu)


def rho_max(xi_b, alpha_1, fc, fy):
    return xi_b * alpha_1 * fc / fy


def rho_min(ft, fy):
    return 0.45 * ft / fy


def Mcr_simplified(alpha_E, As, b, h, ft):
    return 0.292 * (1 + 2.5 * 2 * alpha_E * As / b / h) * ft * b * h ** 2


def Mu(b, h, As, fc, ft, fy, Es, Ec, epsilon_cu, h0):
    _rho_min = rho_min(ft, fy)
    _xi_b = xi_b(beta_1_under_C50(), fy, Es, epsilon_cu)
    _rho_max = rho_max(_xi_b, alpha_1_low(), fc, fy)
    _rho = rho(As, b * h)
    _xi = xi(_rho, fy, alpha_1_low(), fc)
    alpha_E = Es / Ec
    if _rho > _rho_max:
        print("超筋")
        return Mu_over_simplified(fy, _xi, _xi_b, As, alpha_1_low(), fc, b, h0)
    if _rho < _rho_min:
        print("少筋")
        return Mcr_simplified(alpha_E, As, b, h, ft)
    return Mu_fit_simplified(alpha_1_low(), fc, b, h0, _xi)


def Mu_(As_, fy_, h0, as_):
    return fy_ * As_ * (h0 - as_)


def design(b, h, h0, fc, ft, fy, M):
    _rho_min = rho_min(ft, fy)
    # M = fc * b * x * (h0 - x / 2)
    # 2*M/fc/b = x * (2*h0-x)
    # x**2 - 2*h0*x + 2*M/fc/b = 0
    A = 1
    B = -2 * h0
    C = 2 * M / fc / b
    x = (-B - sqrt(B ** 2 - 4 * A * C)) / (2 * A)
    As = fc * b * x / fy
    Mu = fy * As * (h0 - x / 2)
    _rho = rho(As, b * h)
    if _rho < _rho_min:
        print("防止少筋")
        return _rho_min * b * h
    return _rho * b * h

