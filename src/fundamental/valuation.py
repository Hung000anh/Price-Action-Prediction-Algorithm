# macro_valuation.py

import numpy as np

def z_score(series):
    """Chuẩn hóa dữ liệu thành z-score."""
    mean = np.mean(series)
    std = np.std(series)
    if std == 0:
        return np.zeros_like(series)
    return (series - mean) / std

def macro_score(country_data: dict, weights: dict) -> float:
    """
    Tính điểm tổng hợp sức mạnh vĩ mô cho một quốc gia.
    
    Args:
        country_data: dict chứa các chỉ số macro đã chuẩn hóa.
        weights: dict trọng số từng chỉ số.

    Returns:
        float: điểm macro tổng hợp.
    """
    score = 0.0
    for key, weight in weights.items():
        value = country_data.get(key, 0)
        score += weight * value
    return score

def macro_score_diff(data_domestic: dict, data_foreign: dict, weights: dict) -> float:
    """
    Tính điểm chênh lệch sức mạnh macro giữa 2 quốc gia.
    
    Args:
        data_domestic: dict chỉ số quốc gia trong nước.
        data_foreign: dict chỉ số quốc gia đối tác.
        weights: dict trọng số.

    Returns:
        float: chênh lệch điểm (domestic - foreign).
    """
    score_dom = macro_score(data_domestic, weights)
    score_for = macro_score(data_foreign, weights)
    return score_dom - score_for

def fair_value_by_macro(base_fx_rate: float, score_diff: float, sensitivity: float = 0.02) -> float:
    """
    Ước lượng tỷ giá hợp lý dựa trên chênh lệch điểm macro.
    
    Args:
        base_fx_rate: tỷ giá hiện tại (spot).
        score_diff: chênh lệch điểm macro (domestic - foreign).
        sensitivity: hệ số nhạy cảm của tỷ giá theo điểm macro.

    Returns:
        float: tỷ giá hợp lý dự kiến.
    """
    return base_fx_rate * (1 + sensitivity * score_diff)

def is_overvalued(spot: float, fair_value: float, threshold: float = 0.01) -> bool:
    """
    Kiểm tra tiền tệ có đang bị định giá quá cao không.
    """
    deviation = (spot - fair_value) / fair_value
    return deviation > threshold

def is_undervalued(spot: float, fair_value: float, threshold: float = 0.01) -> bool:
    """
    Kiểm tra tiền tệ có đang bị định giá quá thấp không.
    """
    deviation = (spot - fair_value) / fair_value
    return deviation < -threshold

def generate_signal(spot: float, fair_value: float, threshold: float = 0.01) -> str:
    """
    Sinh tín hiệu giao dịch đơn giản dựa trên mức định giá.
    
    Returns:
        "BUY", "SELL", hoặc "HOLD"
    """
    if is_undervalued(spot, fair_value, threshold):
        return "BUY"
    elif is_overvalued(spot, fair_value, threshold):
        return "SELL"
    else:
        return "HOLD"


# --- Ví dụ sử dụng ---

if __name__ == "__main__":
    # Dữ liệu mẫu (bạn thay bằng dữ liệu thực đã chuẩn hóa)
    data_us = {
        "GDP_Growth": 0.5,
        "Interest_Rate": 1.2,
        "Inflation_Rate": -0.3,
        "Unemployment": -0.8,
        "Trade_Balance": 0.2,
        "Consumer_Confidence": 0.4,
        "Money_Supply": -0.1,
    }
    data_eu = {
        "GDP_Growth": 0.3,
        "Interest_Rate": 1.0,
        "Inflation_Rate": -0.1,
        "Unemployment": -0.5,
        "Trade_Balance": 0.3,
        "Consumer_Confidence": 0.5,
        "Money_Supply": 0.0,
    }

    weights = {
        "GDP_Growth": 0.25,
        "Interest_Rate": 0.20,
        "Inflation_Rate": -0.15,
        "Unemployment": -0.15,
        "Trade_Balance": 0.10,
        "Consumer_Confidence": 0.10,
        "Money_Supply": -0.05,
    }

    spot_rate = 1.09  # Ví dụ EURUSD hiện tại
    score_diff = macro_score_diff(data_us, data_eu, weights)
    fair_val = fair_value_by_macro(spot_rate, score_diff)

    print(f"Score difference (US - EU): {score_diff:.3f}")
    print(f"Estimated fair value: {fair_val:.4f}")
    print(f"Current spot rate: {spot_rate}")
    print(f"Trade signal: {generate_signal(spot_rate, fair_val)}")
