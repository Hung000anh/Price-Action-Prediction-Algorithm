"""portfolio_loader.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Module to load historical price data, macro‑economic indicators, and COT data
for a list of financial instruments grouped by category (forex, futures,
crypto, stock).

Functions
---------
load_portfolio_data(category, years, legacy_fut)
    Entry‑point that orchestrates loading price, economic, and COT data for
    every symbol that belongs to *category*.

load_asset_data(symbol, years)
    Download daily / weekly / monthly OHLCV data for a single *symbol*.

load_economic_data(symbol, look_back_bars)
    Fetch a predefined set of macro‑economic indicators that correspond to the
    country / currency behind *symbol*. Automatically converts monetary values
    to USD using the most recent FX rate where required.

load_cot_data(symbol, years, legacy_fut)
    Extract COT (Commitment of Traders) data from an already‑loaded CFTC
    *legacy_fut* DataFrame.

convert_to_usd(value, is_usd_quote, exchange_rate)
    Helper to convert a numeric *value* to USD given the direction of the FX
    quote.
"""

from __future__ import annotations

import pandas as pd
from price_loaders.tradingview import load_asset_price

###############################################################################
# 1️⃣  Danh mục tài sản (PORTFOLIO)                                            #
###############################################################################
# 👉  Mỗi key đại diện cho một nhóm tài sản và mỗi value là danh sách các      #
#      symbol thuộc nhóm đó. Chỉnh sửa tùy nhu cầu.                           #
###############################################################################
PORTFOLIO: dict[str, list[str]] = {
    "forex": [
        "EURUSD",
        # "GBPUSD",
        # "AUDUSD",
        # "NZDUSD",
        # "USDJPY",
        # "USDCAD",
        # "USDCHF",
    ],
    "future": [
        "6E1!",
        "6B1!",
        "6A1!",
        "6N1!",
        "6J1!",
        "6C1!",
        "6S1!",
        "DX1!",
    ],
    "crypto": [
        "BTCUSD",
        "ETHUSD",
        "LTCUSD",
        "SOLUSD",
        "XRPUSD",
    ],
    "stock": [
        "AAPL",
        "TSLA",
        "MSFT",
    ],
}

###############################################################################
# 2️⃣  Hàm load_portfolio_data                                                #
###############################################################################

def load_portfolio_data(
    category: str,
    years: int,
    legacy_fut: pd.DataFrame,
) -> dict[str, dict[str, pd.DataFrame | None]]:
    """Load price, macro‑economic, and COT data for every symbol in *category*.

    Parameters
    ----------
    category : str
        Tên nhóm tài sản, phải tồn tại trong :data:`PORTFOLIO`.
    years : int
        Số năm dữ liệu lịch sử cần lấy (áp dụng cho giá và COT).
    legacy_fut : pandas.DataFrame
        DataFrame chứa toàn bộ dữ liệu COT (bảng *legacy_fut* đã tải sẵn).

    Returns
    -------
    dict[str, dict[str, pandas.DataFrame | None]]
        Kết quả dạng ``{symbol: {"asset_data": ..., "economic_data": ...,
        "cot_data": ...}}``. Nếu hàm con thất bại, giá trị sẽ là *None*.
    """

    if category not in PORTFOLIO:
        raise ValueError(f"Category '{category}' not found in PORTFOLIO.")

    results: dict[str, dict[str, pd.DataFrame | None]] = {}

    for symbol in PORTFOLIO[category]:
        print(f"⏳ Loading data for {symbol}…")

        # -----------------------------------------------------
        # 2.1. Giá tài sản
        # -----------------------------------------------------
        try:
            asset_data = load_asset_data(symbol, years)
        except Exception as exc:  # noqa: BLE001  # broad but intentional
            print(f"❌ Failed to load asset data for {symbol}: {exc}")
            asset_data = None

        # -----------------------------------------------------
        # 2.2. Dữ liệu kinh tế vĩ mô
        # -----------------------------------------------------
        try:
            economic_data = load_economic_data(symbol, look_back_bars=1)
        except Exception as exc:  # noqa: BLE001
            print(f"❌ Failed to load economic data for {symbol}: {exc}")
            economic_data = None

        # -----------------------------------------------------
        # 2.3. Báo cáo COT
        # -----------------------------------------------------
        try:
            cot_data = load_cot_data(symbol, years, legacy_fut)
        except Exception as exc:  # noqa: BLE001
            print(f"❌ Failed to load COT data for {symbol}: {exc}")
            cot_data = None

        # Gộp kết quả
        results[symbol] = {
            "asset_data": asset_data,
            "economic_data": economic_data,
            "cot_data": cot_data,
        }

    return results

###############################################################################
# 3️⃣  Hàm load_asset_data                                                    #
###############################################################################

def load_asset_data(symbol: str, years: int) -> dict[str, pd.DataFrame]:
    """Download daily/weekly/monthly price data for *symbol*.

    Parameters
    ----------
    symbol : str
        Mã giao dịch (ví dụ ``"EURUSD"`` hoặc ``"6E1!"``).
    years : int
        Số năm quá khứ cần tải.

    Returns
    -------
    dict[str, pandas.DataFrame]
        Bao gồm 3 DataFrame: ``{"1D_data": …, "1W_data": …, "1M_data": …}``.

    Raises
    ------
    ValueError
        Nếu *symbol* không có trong *prefix_map* hoặc dữ liệu trả về rỗng.
    """

    # ----------- Ước lượng số bar cần tải cho mỗi timeframe ---------------
    days = years * 252   # xấp xỉ số phiên giao dịch mỗi năm
    weeks = years * 52
    months = years * 12

    # ----------- Ánh xạ symbol → prefix TradingView ------------------------
    prefix_map: dict[str, str] = {
        # Forex (FX:)
        "EURUSD": "FX:",
        "GBPUSD": "FX:",
        "AUDUSD": "FX:",
        "NZDUSD": "FX:",
        "USDJPY": "FX:",
        "USDCAD": "FX:",
        "USDCHF": "FX:",
        # Futures CME
        "6E1!": "CME:",
        "6B1!": "CME:",
        "6A1!": "CME:",
        "6N1!": "CME:",
        "6J1!": "CME:",
        "6C1!": "CME:",
        "6S1!": "CME:",
        # Futures ICEUS
        "DX1!": "ICEUS:",
        # Crypto (Bitstamp)
        "BTCUSD": "BITSTAMP:",
        "ETHUSD": "BITSTAMP:",
        "LTCUSD": "BITSTAMP:",
        "SOLUSD": "BITSTAMP:",
        "XRPUSD": "BITSTAMP:",
    }

    if symbol not in prefix_map:
        raise ValueError(f"Symbol '{symbol}' is not recognized in prefix_map.")

    # ----------- Tải dữ liệu -------------------------------------------------
    prefix = prefix_map[symbol]
    data_1d = load_asset_price(f"{prefix}{symbol}", days, "1D", None)
    data_1w = load_asset_price(f"{prefix}{symbol}", weeks, "1W", None)
    data_1m = load_asset_price(f"{prefix}{symbol}", months, "1M", None)

    # ----------- Kiểm tra dữ liệu ------------------------------------------
    for tf, df in {"1D": data_1d, "1W": data_1w, "1M": data_1m}.items():
        if df is None or df.empty:
            raise ValueError(f"{tf} data for {symbol} is empty.")
        df["time"] = pd.to_datetime(df["time"], utc=True)

    return {"1D_data": data_1d, "1W_data": data_1w, "1M_data": data_1m}

###############################################################################
# 4️⃣  Helper convert_to_usd                                                 #
###############################################################################

def convert_to_usd(value: float, is_usd_quote: bool, exchange_rate: float) -> float:  # noqa: D401,E501
    """Convert *value* sang USD dựa vào *exchange_rate*.

    Nếu cặp forex được quote dưới dạng ``BASE/USD`` (ví dụ *EURUSD*), giá trị
    gốc đang ở *BASE* → cần *nhân* tỷ giá để đổi sang USD. Ngược lại nếu quote
    dạng ``USD/BASE`` (ví dụ *USDJPY*) thì cần *chia*.
    """

    if pd.isna(exchange_rate):
        return value
    return value * exchange_rate if is_usd_quote else value / exchange_rate

###############################################################################
# 5️⃣  Hàm load_economic_data                                                #
###############################################################################

def load_economic_data(symbol: str, look_back_bars: int = 1) -> dict[str, pd.DataFrame]:
    """Fetch macro‑economic indicators for *symbol* and convert to USD.

    Parameters
    ----------
    symbol : str
        Mã giao dịch (forex hoặc future) để suy ra quốc gia / đồng tiền.
    look_back_bars : int, default=1
        Số bar lịch sử cần tải cho mỗi chỉ số. Đối với chuỗi tháng/quý, *1* là
        đủ để lấy giá trị mới nhất.
    """

    # --------------- 5.1. Ánh xạ symbol → (mã quốc gia, tiền tệ bản địa) ----
    country_map: dict[str, tuple[str, str]] = {
        # Spot forex
        "EURUSD": ("EU", "EUR"),
        "GBPUSD": ("GB", "GBP"),
        "AUDUSD": ("AU", "AUD"),
        "NZDUSD": ("NZ", "NZD"),
        "USDJPY": ("JP", "JPY"),
        "USDCAD": ("CA", "CAD"),
        "USDCHF": ("CH", "CHF"),
        # Futures indices
        "DX1!": ("US", "USD"),
        "6E1!": ("EU", "EUR"),
        "6B1!": ("GB", "GBP"),
        "6A1!": ("AU", "AUD"),
        "6N1!": ("NZ", "NZD"),
        "6J1!": ("JP", "JPY"),
        "6C1!": ("CA", "CAD"),
        "6S1!": ("CH", "CHF"),
    }
    if symbol not in country_map:
        raise ValueError(f"Symbol '{symbol}' is not supported in country_map.")

    country_code, base_currency = country_map[symbol]
    prefix = "ECONOMICS:"

    # --------------- 5.2. Danh sách indicator cần tải -----------------------
    indicators: dict[str, tuple[str, str]] = {
        "GDP_Growth": (f"{prefix}{country_code}GDPYY", "3M"),
        "Interest_Rate": (f"{prefix}{country_code}INTR", "1M"),
        "Inflation_Rate": (f"{prefix}{country_code}IRYY", "1M"),
        "CPI": (f"{prefix}{country_code}CPI", "1M"),
        "PPI": (f"{prefix}{country_code}PPI", "1M"),
        "Unemployment": (f"{prefix}{country_code}UR", "1M"),
        "Trade_Balance": (f"{prefix}{country_code}BOT", "1M"),
        "Gov_Debt": (f"{prefix}{country_code}GDG", "12M"),
        "Consumer_Confidence": (f"{prefix}{country_code}CCI", "1M"),
        "Retail_Sales": (f"{prefix}{country_code}RSMM", "1M"),
        "Money_Supply": (
            f"{prefix}{country_code}{'M3' if country_code == 'AU' else 'M2'}",
            "1M",
        ),
    }

    economic_data: dict[str, pd.DataFrame] = {}
    for name, (econ_symbol, timeframe) in indicators.items():
        print(f"Loading {name} → {econ_symbol} ({timeframe})")
        df = load_asset_price(econ_symbol, look_back_bars, timeframe, None)
        if df is not None and not df.empty:
            df["time"] = pd.to_datetime(df["time"], utc=True)
            economic_data[name] = df
        else:
            print(f"⚠️ No data for {name} ({econ_symbol})")

    # --------------- 5.3. Tính tỷ giá mới nhất để quy đổi sang USD ----------
    if base_currency == "USD":  # Đơn vị gốc đã là USD
        exchange_rate_df = None
        is_usd_quote = True
    else:
        pair1, pair2 = f"{base_currency}USD", f"USD{base_currency}"
        if pair1 in PORTFOLIO.get("forex", []):
            forex_symbol, is_usd_quote = pair1, True
        elif pair2 in PORTFOLIO.get("forex", []):
            forex_symbol, is_usd_quote = pair2, False
        else:
            forex_symbol, is_usd_quote = None, True

        exchange_rate_df = (
            load_asset_price(f"FX:{forex_symbol}", look_back_bars, "1D", None)
            if forex_symbol
            else None
        )
        if exchange_rate_df is not None:
            exchange_rate_df["time"] = pd.to_datetime(exchange_rate_df["time"], utc=True)

    # --------------- 5.4. Quy đổi các chỉ số giá trị tiền tệ sang USD -------
    if exchange_rate_df is not None and not exchange_rate_df.empty:
        latest_idx = exchange_rate_df["time"].idxmax()
        latest_rate = exchange_rate_df.loc[latest_idx, "close"]
        print(
            "Latest FX rate",
            f"({forex_symbol})",
            f"{exchange_rate_df.loc[latest_idx, 'time'].date()}: {latest_rate}",
        )

        for key in ("Money_Supply", "Trade_Balance"):
            if key in economic_data:
                df_conv = economic_data[key].copy()
                for col in ("open", "high", "low", "close"):
                    df_conv[col] = df_conv[col].apply(
                        lambda v: convert_to_usd(v, is_usd_quote, latest_rate)
                    )
                economic_data[key] = df_conv
    else:
        print("⚠️ No FX data available → skip USD conversion")

    return economic_data

###############################################################################
# 6️⃣  Hàm load_cot_data                                                     #
###############################################################################

def load_cot_data(symbol: str, years: int, legacy_fut: pd.DataFrame) -> pd.DataFrame:  # noqa: D401,E501
    """Extract COT records that correspond to *symbol* from *legacy_fut*.

    Parameters
    ----------
    symbol : str
        Spot symbol hoặc mã futures (TradingView style).
    years : int
        Số năm lịch sử cần giữ lại.
    legacy_fut : pandas.DataFrame
        Toàn bộ dữ liệu COT (định dạng legacy) tải từ CFTC.
    """

    # --------------- 6.1. Ánh xạ symbol → tên báo cáo COT -------------------
    cot_names: dict[str, str] = {
        # Spot forex
        "EURUSD": "EURO FX - CHICAGO MERCANTILE EXCHANGE",
        "GBPUSD": "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE",
        "USDCHF": "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE",
        "USDJPY": "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE",
        "NZDUSD": "NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE",
        "USDCAD": "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
        "AUDUSD": "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
        # Futures
        "6E1!": "EURO FX - CHICAGO MERCANTILE EXCHANGE",
        "6B1!": "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE",
        "6A1!": "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
        "6N1!": "NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE",
        "6J1!": "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE",
        "6C1!": "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
        "6S1!": "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE",
        "DX1!": "USD INDEX - ICE FUTURES U.S.",
        # Crypto futures (CME)
        "BTCUSD": "BITCOIN - CHICAGO MERCANTILE EXCHANGE",
        "ETHUSD": "ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE",
    }

    if symbol not in cot_names:
        print(f"⚠️ Symbol {symbol} is not in COT mapping → skip")
        return None

    report_name: str = cot_names[symbol]

    # --------------- 6.2. Lọc legacy_fut theo report_name -------------------
    mask = legacy_fut["Market and Exchange Names"].str.contains(
        report_name, case=False, na=False
    )
    cot_raw = legacy_fut.loc[mask].copy()
    if cot_raw.empty:
        raise ValueError(f"❌ No COT data found for '{symbol}' ({report_name})")

    # --------------- 6.3. Chuẩn hóa cột -------------------------------------
    rename_map = {
        "As of Date in Form YYYY-MM-DD": "date",
        "Commercial Positions-Long (All)": "commercial_long",
        "Commercial Positions-Short (All)": "commercial_short",
        "Noncommercial Positions-Long (All)": "noncommercial_long",
        "Noncommercial Positions-Short (All)": "noncommercial_short",
        "Nonreportable Positions-Long (All)": "retail_long",
        "Nonreportable Positions-Short (All)": "retail_short",
        "Open Interest (All)": "open_interest",
    }
    cot_raw.rename(columns=rename_map, inplace=True)

    cot_raw["date"] = pd.to_datetime(cot_raw["date"], utc=True)

    # --------------- 6.4. Giữ lại *years* năm gần đây ----------------------
    min_date = pd.Timestamp.utcnow() - pd.DateOffset(years=years)
    cot_trimmed = cot_raw[cot_raw["date"] >= min_date].copy()

    return cot_trimmed.reset_index(drop=True)
