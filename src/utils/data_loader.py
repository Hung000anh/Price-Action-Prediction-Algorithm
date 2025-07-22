import pandas as pd
from price_loaders.tradingview import load_asset_price

# 1. Định nghĩa danh mục (portfolio categories)
PORTFOLIO = {
    "forex": ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDJPY", "USDCAD", "USDCHF"],
    "crypto": ["BTCUSD", "ETHUSD", "LTCUSD"],  # ví dụ
    "stock": ["AAPL", "TSLA", "MSFT"],       # ví dụ
}

# 2. Hàm load dữ liệu cho nhiều symbol trong 1 danh mục
def load_portfolio_data(category, years, legacy_fut):
    if category not in PORTFOLIO:
        raise ValueError(f"Danh mục '{category}' chưa được định nghĩa.")
    
    symbols = PORTFOLIO[category]
    
    data = {}
    for symbol in symbols:
        try:
            data[symbol] = load_data(symbol, years, legacy_fut)
        except Exception as e:
            print(f"Lỗi khi tải {symbol}: {e}")
            data[symbol] = None
    return data


def load_data(symbol: str, years: int, legacy_fut=None):
    if legacy_fut is None:
            raise ValueError("legacy_fut phải được truyền vào để tránh tải lại dữ liệu.")

    # Hợp lệ symbol
    valid_symbols = {"EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF", "NZDUSD", "USDCAD"}
    if symbol not in valid_symbols:
        raise ValueError(f"Symbol '{symbol}' không hợp lệ hoặc chưa được hỗ trợ.")
    
    # Thời gian tương ứng
    days = years * 252
    weeks = years * 52
    months = years * 12

    # Tải dữ liệu theo từng timeframe
    data_D = load_asset_price(symbol, days, "1D", None)
    data_W = load_asset_price(symbol, weeks, "1W", None)
    data_M = load_asset_price(symbol, months, "1M", None)
    
    # Kiểm tra dữ liệu không rỗng
    if data_D is None or data_D.empty:
        raise ValueError(f"Dữ liệu ngày cho '{symbol}' trống hoặc không hợp lệ.")
    if data_W is None or data_W.empty:
        raise ValueError(f"Dữ liệu tuần cho '{symbol}' trống hoặc không hợp lệ.")
    if data_M is None or data_M.empty:
        raise ValueError(f"Dữ liệu tháng cho '{symbol}' trống hoặc không hợp lệ.")
    
    # Chuyển đổi cột thời gian
    data_D['time'] = pd.to_datetime(data_D['time'])
    data_W['time'] = pd.to_datetime(data_W['time'])
    data_M['time'] = pd.to_datetime(data_M['time'])

    # CoT mapping
    cot_names = {
        'EURUSD': 'EURO FX - CHICAGO MERCANTILE EXCHANGE',
        'GBPUSD': 'BRITISH POUND - CHICAGO MERCANTILE EXCHANGE',
        'USDCHF': 'SWISS FRANC - CHICAGO MERCANTILE EXCHANGE',
        'USDJPY': 'JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE',
        'NZDUSD': 'NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE',
        'USDCAD': 'CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE',
        'AUDUSD': 'AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE'
    }


    if symbol in cot_names:
        cot_data = legacy_fut[
            legacy_fut['Market and Exchange Names'].str.contains(cot_names[symbol], case=False)
        ].copy()

        cot_data.rename(columns={
            'As of Date in Form YYYY-MM-DD': 'date',
            'Commercial Positions-Long (All)': 'commercial_long',
            'Commercial Positions-Short (All)': 'commercial_short',
            'Noncommercial Positions-Long (All)': 'noncommercial_long',
            'Noncommercial Positions-Short (All)': 'noncommercial_short',
            'Nonreportable Positions-Long (All)': 'retail_long',
            'Nonreportable Positions-Short (All)': 'retail_short',
            'Open Interest (All)': 'open_interest',
        }, inplace=True)

        cot_data['date'] = pd.to_datetime(cot_data['date'])

        # Lọc CoT theo số năm
        min_date = pd.Timestamp.today() - pd.DateOffset(years=years)
        cot_data = cot_data[cot_data['date'] >= min_date].copy()
    else:
        cot_data = None

    return {
        "1D_data": data_D,
        "1W_data": data_W,
        "1M_data": data_M,
        "COT_data": cot_data
    }
