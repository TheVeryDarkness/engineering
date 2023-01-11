from math import pi, sqrt, tan


def calculate(h: int | float, hT1: int | float, phi: int | float, gamma: int | float):
    Kp = tan((pi / 2 + phi) / 2) ** 2
    Ka = tan((pi / 2 - phi) / 2) ** 2
    hc1 = Ka * h / (Kp - Ka)
    dT1 = h - hT1

    Ep = Kp * hc1 ** 2
    Ea = Ka * (h + hc1) ** 2
    Rc = (
        (Ea * (2 / 3 * h + 2 / 3 * hc1 - dT1) - Ep * (h + 2 / 3 * hc1 - dT1))
        * gamma
        / 2
        / (h + hc1 - dT1)
    )
    h0 = sqrt(6 * Rc / gamma / (Kp - Ka))
    hd = hc1 + 1.2 * h0
    print(
        f"""
Kp  = {Kp}
Ka  = {Ka}
hc1 = {hc1}
Ep  = {Ep}
Ea  = {Ea}
Rc  = {Rc}
h0  = {h0}
hd  = {hd}
"""
    )
