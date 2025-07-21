import pandas as pd
import numpy as np
import plotly.graph_objects as go

def plot_cot_index_with_extremes_plotly(df, start_date='2025-01-01', end_date=None, weeks=26, 
                                        upperExtreme=80, lowerExtreme=20):
    df = df.copy()
    df.rename(columns={
        'As of Date in Form YYYY-MM-DD': 'date',
        'Commercial Positions-Long (All)': 'commercial_long',
        'Commercial Positions-Short (All)': 'commercial_short',
        'Noncommercial Positions-Long (All)': 'noncommercial_long',
        'Noncommercial Positions-Short (All)': 'noncommercial_short',
        'Nonreportable Positions-Long (All)': 'retail_long',
        'Nonreportable Positions-Short (All)': 'retail_short',
        'Open Interest (All)': 'open_interest',
    }, inplace=True)

    df['date'] = pd.to_datetime(df['date'])

    # 1. Resample dữ liệu theo tuần (thứ Sáu)
    df_weekly = df.set_index('date').resample('W-FRI').last().dropna().reset_index()

    # 2. Tính net positions
    df_weekly['net_commercial'] = df_weekly['commercial_long'] - df_weekly['commercial_short']
    df_weekly['net_large'] = df_weekly['noncommercial_long'] - df_weekly['noncommercial_short']
    df_weekly['net_retail'] = df_weekly['retail_long'] - df_weekly['retail_short']

    # 3. Normalize theo open interest
    df_weekly['adj_commercial'] = df_weekly['net_commercial'] / df_weekly['open_interest'].replace(0, np.nan)
    df_weekly['adj_large'] = df_weekly['net_large'] / df_weekly['open_interest'].replace(0, np.nan)
    df_weekly['adj_retail'] = df_weekly['net_retail'] / df_weekly['open_interest'].replace(0, np.nan)

    # 4. Tính chỉ số COT Index
    def calc_index(adj_net_pos):
        min_val = adj_net_pos.rolling(window=weeks, min_periods=1).min()
        max_val = adj_net_pos.rolling(window=weeks, min_periods=1).max()
        idx = 100 * (adj_net_pos - min_val) / (max_val - min_val)
        idx[max_val == min_val] = np.nan
        return idx

    df_weekly['cot_index_commercial'] = calc_index(df_weekly['adj_commercial'])
    df_weekly['cot_index_large'] = calc_index(df_weekly['adj_large'])
    df_weekly['cot_index_retail'] = calc_index(df_weekly['adj_retail'])

    # 5. Lọc theo thời gian
    if end_date:
        mask = (df_weekly['date'] >= pd.to_datetime(start_date)) & (df_weekly['date'] <= pd.to_datetime(end_date))
    else:
        mask = df_weekly['date'] >= pd.to_datetime(start_date)
    df_ = df_weekly.loc[mask].copy()

    # 6. Vùng cực trị
    def find_regions(mask, dates):
        regions = []
        start = None
        for i, val in enumerate(mask):
            if val and start is None:
                start = dates.iat[i]
            elif not val and start is not None:
                end = dates.iat[i-1]
                regions.append((start, end))
                start = None
        if start is not None:
            regions.append((start, dates.iat[-1]))
        return regions

    bullish_mask = (df_['cot_index_commercial'] >= upperExtreme) & (df_['cot_index_retail'] <= lowerExtreme)
    bearish_mask = (df_['cot_index_commercial'] <= lowerExtreme) & (df_['cot_index_retail'] >= upperExtreme)

    bullish_regions = find_regions(bullish_mask.values, df_['date'])
    bearish_regions = find_regions(bearish_mask.values, df_['date'])

    # 7. Plot bằng Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_['date'], y=df_['cot_index_commercial'],
                             mode='lines', name='Commercial', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df_['date'], y=df_['cot_index_large'],
                             mode='lines', name='Large Speculators', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df_['date'], y=df_['cot_index_retail'],
                             mode='lines', name='Retail', line=dict(color='blue')))

    # Vùng cực trị
    for start, end in bullish_regions:
        fig.add_vrect(x0=start, x1=end, fillcolor='blue', opacity=0.2, line_width=0)
    for start, end in bearish_regions:
        fig.add_vrect(x0=start, x1=end, fillcolor='red', opacity=0.2, line_width=0)

    # Đường ngưỡng
    fig.add_hline(y=upperExtreme, line_dash="dash", line_color="gray")
    fig.add_hline(y=lowerExtreme, line_dash="dash", line_color="gray")

    fig.update_layout(
        title=f"CoT Index with Extreme Zones ({start_date} to {end_date or 'latest'})",
        xaxis_title="Date",
        yaxis_title="CoT Index (%)",
        template="plotly_white",
        height=500,
        width=1000,
        legend=dict(x=0.01, y=0.99)
    )

    fig.show()