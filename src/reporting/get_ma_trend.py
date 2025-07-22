import pandas as pd
from technical.moving_averages import moving_averages
def get_ma_trend(df, timeframe):
    df = df.copy()
    df = moving_averages(df)
    df['time'] = pd.to_datetime(df['time'])

    last_date = df['time'].max()

    if timeframe == 'D':
        mask = (df['time'].dt.month != last_date.month) | (df['time'].dt.year != last_date.year)
    elif timeframe == 'W':
        current_quarter = (last_date.month - 1) // 3 + 1
        mask = ~((df['time'].dt.year == last_date.year) & ((df['time'].dt.month - 1) // 3 + 1 == current_quarter))
    elif timeframe == 'M':
        mask = df['time'].dt.year < last_date.year
    else:
        return None

    df = df[mask].dropna(subset=['MA30', 'MA60', 'MA90'])
    if df.empty:
        return None

    row = df.iloc[-1]
    ma30 = row['MA30']
    ma60 = row['MA60']
    ma90 = row['MA90']
    time_str = row['time'].strftime('%Y-%m-%d')

    if ma30 > ma90 and ma60 > ma90:
        trend = 'Uptrend'
    elif ma30 < ma90 and ma60 < ma90:
        trend = 'Downtrend'
    elif (ma30 > ma90 and ma60 < ma90) or (ma30 < ma90 and ma60 > ma90):
        trend = 'Sideways'
    else:
        trend = 'Unknown'

    return f"{trend}\nDate: {time_str} \nMA30: {ma30:.5f}\nMA60: {ma60:.5f}\nMA90: {ma90:.5f}"
