import pandas as pd
from price_loaders.tradingview import load_asset_price

# 1. Định nghĩa danh mục (portfolio categories)
PORTFOLIO = {
    "forex": ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDJPY", "USDCAD", "USDCHF"],
    "future": ["6E1!", "6B1!", "6A1!", "6N1!", "6J1!", "6C1!", "6S1!", "DX1!"],
    "crypto": ["BTCUSD", "ETHUSD", "LTCUSD", "SOLUSD", "XRPUSD"],  # ví dụ
    "stock": ["AAPL", "TSLA", "MSFT"],       # ví dụ
}

# 2. Hàm load dữ liệu cho nhiều symbol trong 1 danh mục
def load_portfolio_data(category, years, legacy_fut):
    if category not in PORTFOLIO:
        raise ValueError(f"Category '{category}' not found in portfolio.")

    results = {}

    for symbol in PORTFOLIO[category]:
        print(f"⏳ Loading data for {symbol}...")

        try:
            asset_data = load_asset_data(symbol, years)
        except Exception as e:
            print(f"❌ Failed to load asset data for {symbol}: {e}")
            asset_data = None  # ✅ Rõ ràng hơn

        try:
            economic_data = load_economic_data(symbol, years)
        except Exception as e:
            print(f"❌ Failed to load economic data for {symbol}: {e}")
            economic_data = None

        try:
            cot_data = load_cot_data(symbol, years, legacy_fut)
        except Exception as e:
            print(f"❌ Failed to load COT data for {symbol}: {e}")
            cot_data = None

        results[symbol] = {
            "asset_data": asset_data,
            "economic_data": economic_data,
            "cot_data": cot_data,
        }

    return results


def load_asset_data(symbol, years):

    # Estimate the number of data points for each timeframe
    days = years * 252       # Approx. number of trading days in a year
    weeks = years * 52       # Approx. number of trading weeks
    months = years * 12      # Number of months

    # Prefix mapping based on symbol types
    prefix_map = {
        # Forex symbols (FX:)
        "EURUSD": "FX:",
        "GBPUSD": "FX:",
        "AUDUSD": "FX:",
        "NZDUSD": "FX:",
        "USDJPY": "FX:",
        "USDCAD": "FX:",
        "USDCHF": "FX:",

        # Futures (CME:)
        "6E1!": "CME:",
        "6B1!": "CME:",
        "6A1!": "CME:",
        "6N1!": "CME:",
        "6J1!": "CME:",
        "6C1!": "CME:",
        "6S1!": "CME:",
        # Futures (ICEUS:)
        "DX1!": "ICEUS:",

        # Crypto
        "BTCUSD": "CRYPTO:",
        "ETHUSD": "CRYPTO:",
        "LTCUSD": "CRYPTO:", 
        "SOLUSD": "CRYPTO:", 
        "XRPUSD": "CRYPTO:"
    }

    # Get the prefix for the given symbol
    if symbol not in prefix_map:
        raise ValueError(f"Symbol '{symbol}' is not recognized in prefix_map.")

    prefix = prefix_map[symbol]

    # Load historical price data
    data_D = load_asset_price(prefix + symbol, days, "1D", None)
    data_W = load_asset_price(prefix + symbol, weeks, "1W", None)
    data_M = load_asset_price(prefix + symbol, months, "1M", None)

    # Basic validation
    if data_D is None or data_D.empty:
        raise ValueError(f"Daily data for {symbol} is empty.")
    if data_W is None or data_W.empty:
        raise ValueError(f"Weekly data for {symbol} is empty.")
    if data_M is None or data_M.empty:
        raise ValueError(f"Monthly data for {symbol} is empty.")

    # Ensure datetime format
    data_D['time'] = pd.to_datetime(data_D['time'])
    data_W['time'] = pd.to_datetime(data_W['time'])
    data_M['time'] = pd.to_datetime(data_M['time'])

    return {
        "1D_data": data_D,
        "1W_data": data_W,
        "1M_data": data_M,
    }


def load_economic_data(symbol, years):
    """
    Load macroeconomic data (e.g., GDP, Interest Rate, CPI, PPI, Unemployment, etc.)
    based on a given forex/futures symbol.

    Parameters:
        symbol (str): Asset symbol (e.g., 'EURUSD', '6E1!', etc.)
        years (int): Number of years of historical data to retrieve.

    Returns:
        dict: Dictionary of economic dataframes for different indicators.
    """

    # Mapping trading symbols to their corresponding country code
    country_map = {
        "EURUSD": "EU",
        "GBPUSD": "GB",
        "AUDUSD": "AU",
        "NZDUSD": "NZ",
        "USDJPY": "JP",
        "USDCAD": "CA",
        "USDCHF": "CH",
        
        "DX1!": "US",   # Dollar Index
        "6E1!": "EU",   # Euro futures
        "6B1!": "GB",   # Pound futures
        "6A1!": "AU",   # Aussie futures
        "6N1!": "NZ",   # Kiwi futures
        "6J1!": "JP",   # Yen futures
        "6C1!": "CA",   # CAD futures
        "6S1!": "CH",   # CHF futures
    }

    # Check if the symbol is supported
    if symbol not in country_map:
        raise ValueError(f"Symbol '{symbol}' is not supported in country_map.")

    # Get the country code
    country_code = country_map[symbol]
    prefix = "ECONOMICS:"
    months = years * 12

    # Define the macroeconomic indicators and their timeframes
    indicators = {
        "GDP_Growth":      (prefix + country_code + "GDPYY", "3M"),
        "Interest_Rate":   (prefix + country_code + "INTR", "1M"),
        "Inflation_Rate":  (prefix + country_code + "IRYY", "1M"),
        "CPI":             (prefix + country_code + "CPI", "1M"),
        "PPI":             (prefix + country_code + "PPI", "1M"),
        "Unemployment":    (prefix + country_code + "UR", "1M"),
        "Trade_Balance":   (prefix + country_code + "BOT", "1M"),
        "Gov_Debt":        (prefix + country_code + "GDG", "12M"),
        "Consumer_Confidence": (prefix + country_code + "CCI", "1M"),
        "Retail_Sales":    (prefix + country_code + "RSMM", "1M"),
        "Money_Supply":    (prefix + country_code + ("M3" if country_code == "AU" else "M2"), "1M"),
    }

    # Initialize the output dictionary
    economic_data = {}

    # Loop through indicators and load data
    for name, (econ_symbol, timeframe) in indicators.items():
        print(f"Loading {name} data with symbol: {econ_symbol}, TF: {timeframe}")
        data = load_asset_price(econ_symbol, months, timeframe, None)
        if data is not None and not data.empty:
            data["time"] = pd.to_datetime(data["time"])
            economic_data[name] = data
        else:
            print(f"Warning: No data found for {name} ({econ_symbol})")

    return economic_data


def load_cot_data(symbol, years, legacy_fut):
    # Mapping from trading symbols to official COT report names
    cot_names = {
        # Forex spot pairs
        'EURUSD': 'EURO FX - CHICAGO MERCANTILE EXCHANGE',
        'GBPUSD': 'BRITISH POUND - CHICAGO MERCANTILE EXCHANGE',
        'USDCHF': 'SWISS FRANC - CHICAGO MERCANTILE EXCHANGE',
        'USDJPY': 'JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE',
        'NZDUSD': 'NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE',
        'USDCAD': 'CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE',
        'AUDUSD': 'AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE',

        # Futures symbols (e.g., TradingView-style)
        '6E1!': 'EURO FX - CHICAGO MERCANTILE EXCHANGE',
        '6B1!': 'BRITISH POUND - CHICAGO MERCANTILE EXCHANGE',
        '6A1!': 'AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE',
        '6N1!': 'NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE',
        '6J1!': 'JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE',
        '6C1!': 'CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE',
        '6S1!': 'SWISS FRANC - CHICAGO MERCANTILE EXCHANGE',
        'DX1!': 'USD INDEX - ICE FUTURES U.S.',

        # Crypto
        "BTCUSD" : "BITCOIN - CHICAGO MERCANTILE EXCHANGE", 
        "ETHUSD" : "ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE", 
        # "LTCUSD", 
        # "SOLUSD", 
        # "XRPUSD"
    }

    # Check if the symbol exists in the mapping
    if symbol not in cot_names:
        print(f"⚠️ Symbol {symbol} is not available in the COT mapping list.")
        return None

    report_name = cot_names[symbol]

    # Filter COT data for the specific market/exchange name
    cot_data = legacy_fut[
        legacy_fut['Market and Exchange Names'].str.contains(report_name, case=False, na=False)
    ].copy()

    # Raise error if data is not found
    if cot_data.empty:
        raise ValueError(f"❌ No COT data found for {symbol} ({report_name})")

    # Rename columns for easier handling
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

    # Convert date column to datetime
    cot_data['date'] = pd.to_datetime(cot_data['date'])

    # Filter data by number of years
    min_date = pd.Timestamp.today() - pd.DateOffset(years=years)
    cot_data = cot_data[cot_data['date'] >= min_date].copy()

    return cot_data.reset_index(drop=True)




# def load_portfolio_data(category, years, legacy_fut):
#     if category not in PORTFOLIO:
#         raise ValueError(f"Danh mục '{category}' chưa được định nghĩa.")
    
#     symbols = PORTFOLIO[category]
    
#     data = {}
#     for symbol in symbols:
#         try:
#             data[symbol] = load_data(symbol, years, legacy_fut)
#         except Exception as e:
#             print(f"Lỗi khi tải {symbol}: {e}")
#             data[symbol] = None
#     return data


# def load_data(symbol: str, years: int, legacy_fut=None):
#     if legacy_fut is None:
#             raise ValueError("legacy_fut phải được truyền vào để tránh tải lại dữ liệu.")

#     # Hợp lệ symbol
#     valid_symbols = {"EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF", "NZDUSD", "USDCAD"}
#     if symbol not in valid_symbols:
#         raise ValueError(f"Symbol '{symbol}' không hợp lệ hoặc chưa được hỗ trợ.")
    
#     # Thời gian tương ứng
#     days = years * 252
#     weeks = years * 52
#     months = years * 12

#     # Tải dữ liệu theo từng timeframe
#     data_D = load_asset_price(symbol, days, "1D", None)
#     data_W = load_asset_price(symbol, weeks, "1W", None)
#     data_M = load_asset_price(symbol, months, "1M", None)
    
#     # Kiểm tra dữ liệu không rỗng
#     if data_D is None or data_D.empty:
#         raise ValueError(f"Dữ liệu ngày cho '{symbol}' trống hoặc không hợp lệ.")
#     if data_W is None or data_W.empty:
#         raise ValueError(f"Dữ liệu tuần cho '{symbol}' trống hoặc không hợp lệ.")
#     if data_M is None or data_M.empty:
#         raise ValueError(f"Dữ liệu tháng cho '{symbol}' trống hoặc không hợp lệ.")
    
#     # Chuyển đổi cột thời gian
#     data_D['time'] = pd.to_datetime(data_D['time'])
#     data_W['time'] = pd.to_datetime(data_W['time'])
#     data_M['time'] = pd.to_datetime(data_M['time'])

#     # CoT mapping
#     cot_names = {
#         'EURUSD': 'EURO FX - CHICAGO MERCANTILE EXCHANGE',
#         'GBPUSD': 'BRITISH POUND - CHICAGO MERCANTILE EXCHANGE',
#         'USDCHF': 'SWISS FRANC - CHICAGO MERCANTILE EXCHANGE',
#         'USDJPY': 'JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE',
#         'NZDUSD': 'NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE',
#         'USDCAD': 'CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE',
#         'AUDUSD': 'AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE'
#     }


#     if symbol in cot_names:
#         cot_data = legacy_fut[
#             legacy_fut['Market and Exchange Names'].str.contains(cot_names[symbol], case=False)
#         ].copy()

#         cot_data.rename(columns={
#             'As of Date in Form YYYY-MM-DD': 'date',
#             'Commercial Positions-Long (All)': 'commercial_long',
#             'Commercial Positions-Short (All)': 'commercial_short',
#             'Noncommercial Positions-Long (All)': 'noncommercial_long',
#             'Noncommercial Positions-Short (All)': 'noncommercial_short',
#             'Nonreportable Positions-Long (All)': 'retail_long',
#             'Nonreportable Positions-Short (All)': 'retail_short',
#             'Open Interest (All)': 'open_interest',
#         }, inplace=True)

#         cot_data['date'] = pd.to_datetime(cot_data['date'])

#         # Lọc CoT theo số năm
#         min_date = pd.Timestamp.today() - pd.DateOffset(years=years)
#         cot_data = cot_data[cot_data['date'] >= min_date].copy()
#     else:
#         cot_data = None

#     return {
#         "1D_data": data_D,
#         "1W_data": data_W,
#         "1M_data": data_M,
#         "COT_data": cot_data
#     }
