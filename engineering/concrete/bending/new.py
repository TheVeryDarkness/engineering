# -*- encoding=utf-8 -*-


from .. import utils
from math import floor, pi, sqrt


"""
Simplified formulas only

b  宽度（腹板或梁）
h  高度
as 受拉区钢筋合力作用点距离

Es  受拉钢筋弹性模量
fc  混凝土受压强度设计值
fcu 混凝土立方体受压强度（标号）
εcu 混凝土受压极限应变
fy  受拉钢筋屈服强度

双筋：
    as_ = as' 受压区钢筋合力作用点距离
    fy_ = fy' 受压钢筋屈服强度
    As_ = As' 受压钢筋截面面积

"""


@utils.log
def 单筋矩形截面受弯承载力(**kwargs):
    """
    单筋双筋均可用
    """
    __fcu: int = kwargs["fcu"]
    __α1, __β1 = utils.get_α1_and_β1(__fcu)
    __fy: float | int = kwargs["fy"]
    __As: float = kwargs["As"]
    __as: float = kwargs["as"]
    __b: float | int = kwargs["b"]
    __h: float | int = kwargs["h"]

    __Mu_: float = 0.0

    __fc: float = kwargs["fc"]
    # α1 fc b x = fy As1
    __x = __fy * __As / __α1 / __fc / __b
    __Es: float = kwargs["Es"]
    __εcu: float = kwargs["εcu"]
    __ξb = utils.__get_ξb(__β1, __fy, __Es, __εcu)
    __xb = __ξb * (__h - __as)
    if __x > __xb:
        print("超筋")
        # x 需要重新计算
        # σs = fy * (ξ - 0.8) / (ξb - 0.8)
        # σs As = α1 fc b ξ h0
        # 代入得
        # fy * As * (ξ - 0.8) / (ξb - 0.8) = α1 fc b ξ h0
        # (fy * As - α1 fc b h0 * (ξb - 0.8)) ξ = 0.8 fy As
        __ξ = (
            0.8
            * __fy
            * __As
            / (__fy * __As - __α1 * __fc * __b * (__h - __as) * (__ξb - 0.8))
        )
        __σs = __fy * (__ξ - 0.8) / (__ξb - 0.8)
        __x = __ξ * (__h - __as)
        __Mu1 = __σs * __As * (__h - __as - __x / 2)
        return __Mu1 + __Mu_
    # 适筋截面
    print("适筋")
    __Mu1 = __fy * __As * (__h - __as - __x / 2)
    return __Mu1 + __Mu_


@utils.log
def 单筋矩形截面受拉纵筋设计(**kwargs):
    __fcu = kwargs["fcu"]
    __fc = kwargs["fc"]
    __b = kwargs["b"]
    __h = kwargs["h"]
    __α1, __β1 = utils.get_α1_and_β1(__fcu)
    __Es = kwargs["Es"]
    __εcu = kwargs["εcu"]
    __fy = kwargs["fy"]
    __ξb = utils.get_ξb(β1=__β1, fy=__fy, Es=__Es, εcu=__εcu)

    max_As_1 = floor(__b / 35) * pi * 20 ** 2
    max_x_1 = max_As_1 * __fy / (__α1 * __fc * __b)
    __M = kwargs["M"]

    __h0 = kwargs.get(
        "h0", __h - 35 if __fy * max_As_1 * (__h - 35 - max_x_1 / 2) > __M else __h - 60
    )
    __Mu_max = __α1 * __fc * __b * __h0 ** 2 * __ξb * (1 - __ξb / 2)
    if __M > __Mu_max:
        raise utils.DesignFailure("承受弯矩过大")
    # α1 fc b x = fy As
    # M < Mu = α1 fc b x (h0 - x / 2)
    # x (x - 2 * h0) < -2M / (α1 fc b)
    # (x - h0)**2 < h0**2 - 2 M / (α1 fc b)
    # x > h0 - sqrt(h0**2 - 2 M / (α1 fc b))
    __x = __h0 - sqrt(__h0 ** 2 - 2 * __M / (__α1 * __fc * __b))
    __As = __α1 * __fc * __b * __x / __fy
    return __As


@utils.log
def 双筋矩形截面受弯承载力(**kwargs):
    """
    单筋双筋均可用
    """
    __fcu: int = kwargs["fcu"]
    __α1, __β1 = utils.get_α1_and_β1(__fcu)
    __fy: float | int = kwargs["fy"]
    __As: float = kwargs["As"]
    __as: float = kwargs["as"]
    __b: float | int = kwargs["b"]
    __h: float | int = kwargs["h"]

    __As1 = __As
    __Mu_: float = 0.0
    if "As_" in kwargs:
        print("As_ 已定义，为双筋截面。")
        __as_: float = kwargs["as_"]
        __As_: float = kwargs["As_"]
        __fy_: float = kwargs["fy_"]
        __As2 = __fy_ * __As_ / __fy
        __As1 = __As - __As2
        # 只考虑两部分钢筋间的力矩
        __Mu_ = __fy_ * __As_ * (__h - __as - __as_)
    else:
        print("As_ 未定义，为单筋截面。")

    __fc: float = kwargs["fc"]
    # α1 fc b x = fy As1
    __x = __fy * __As1 / __α1 / __fc / __b
    __Es: float = kwargs["Es"]
    __εcu: float = kwargs["εcu"]
    if "as_" in kwargs:
        __as_ = kwargs["as_"]
        if __x < 2 * __as_:
            print("受压钢筋不能保证屈服")
            # x 需要重新计算
            # 几何关系
            # xn : (xn - as') = εcu : εs'
            # σs' = Es * εcu * (1 - β1 * as' / x)
            # 力平衡
            # α1 fc b x = fy As + σs' As'
            # α1 fc b x = fy As + As' Es εcu (β1 as' / x - 1)
            # α1 fc b x^2 = fy As x + As' Es εcu (β1 as' - x)
            # α1 fc b x^2 + As' Es εcu x - fy As x - As' Es εcu β1 as' = 0
            # 两根一正一负，取较大根
            __x = utils.__get_larger_root(
                __α1 * __fc * __b,
                __As_ * __Es * __εcu - __fy * __As1,
                -__As_ * __Es * __εcu * __β1 * __as_,
            )
            __σs_ = (__α1 * __fc * __b * __x - __fy * __As1) / __As_
            __Mu = __α1 * __fc * __b * __x * (__h - __as - __x / 2) - __σs_ * __As_ * (
                __h - __as - __as_
            )
            return __Mu
    __ξb = utils.__get_ξb(__β1, __fy, __Es, __εcu)
    __xb = __ξb * (__h - __as)
    if __x > __xb:
        print("单筋部分超筋")
        # x 需要重新计算
        # σs = fy * (ξ - 0.8) / (ξb - 0.8)
        # σs As = α1 fc b ξ h0
        # 代入得
        # fy * As * (ξ - 0.8) / (ξb - 0.8) = α1 fc b ξ h0
        # (fy * As - α1 fc b h0 * (ξb - 0.8)) ξ = 0.8 fy As
        __ξ = (
            0.8
            * __fy
            * __As1
            / (__fy * __As1 - __α1 * __fc * __b * (__h - __as) * (__ξb - 0.8))
        )
        __σs = __fy * (__ξ - 0.8) / (__ξb - 0.8)
        __x = __ξ * (__h - __as)
        __Mu1 = __σs * __As1 * (__h - __as - __x / 2)
        return __Mu1 + __Mu_
    # 适筋截面
    print("单筋部分适筋")
    __Mu1 = __fy * __As1 * (__h - __as - __x / 2)
    return __Mu1 + __Mu_


@utils.log
def 单筋T形截面受弯承载力(**kwargs):
    __fcu: int = kwargs["fcu"]
    __α1, __β1 = utils.get_α1_and_β1(__fcu)
    __fy: float | int = kwargs["fy"]
    __As: float = kwargs["As"]
    __as: float = kwargs["as"]
    __b: float | int = kwargs["b"]
    __h: float | int = kwargs["h"]

    __bf_: float | int = kwargs["bf_"]
    if "l0" in kwargs:
        __l0 = kwargs["l0"]
        __max_bf_ = __l0 / 3
        if __bf_ > __max_bf_:
            print(f"受压翼缘计算宽度根据计算跨度由{__bf_}截断到{__max_bf_}")
            __bf_ = __max_bf_
    else:
        print("计算跨度 l0 未定义。")

    __hf_: float | int = kwargs["hf_"]
    __max_bf_ = __b + 12 * __hf_
    if __bf_ > __max_bf_:
        print(f"受压翼缘计算宽度根据翼缘高度由{__bf_}截断到{__max_bf_}")

    __fc: float = kwargs["fc"]
    __ft: float = kwargs["ft"]

    __ρmin = utils.get_ρmin(__ft, __fy)
    # fy As = α1 fc b x 与 α1 fc bf' hf' 相比
    if __fy * __As <= __α1 * __fc * __bf_ * __hf_:  # 第一类
        return 单筋矩形截面受弯承载力(b=__bf_, **kwargs)
    else:
        __Mu1 = 单筋矩形截面受弯承载力(**kwargs)
        __Muf_ = __α1 * __fc * (__bf_ - __b) * __hf_
        return __Mu1 + __Muf_
