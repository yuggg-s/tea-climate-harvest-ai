"""
积温计算模块
基于茶树生长起点温度计算有效积温，用于判断采摘窗口期
"""
import pandas as pd


def calc_accum_temp(df: pd.DataFrame, base_temp: float = 10.0) -> float:
    """
    计算有效积温（活动积温法）

    茶树芽头萌动起点温度约为 10°C，低于此温度不计入有效积温。
    有效积温 = Σ max(0, 日均温 - 起点温度)

    参数：
        df: 气象数据 DataFrame，必须包含 'temp_avg' 列
        base_temp: 茶树生长起点温度，默认 10°C

    返回：
        累计有效积温（°C·d）
    """
    if "temp_avg" not in df.columns:
        raise ValueError("气象数据缺少 'temp_avg' 列，请检查 CSV 字段名")

    # 逐日计算有效温度，低于起点温度按 0 计
    effective = df["temp_avg"].apply(lambda t: max(0.0, float(t) - base_temp))
    return float(effective.sum())