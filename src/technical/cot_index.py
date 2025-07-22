import numpy as np
import pandas as pd

def cot_index(cot_df, weeks=26):
    # Đổi tên cột để dễ thao tác (bạn có thể điều chỉnh theo dữ liệu thực tế)
    cot_df = cot_df.rename(columns={
        'As of Date in Form YYYY-MM-DD': 'date',
        'Commercial Positions-Long (All)': 'commercial_long',
        'Commercial Positions-Short (All)': 'commercial_short',
        'Noncommercial Positions-Long (All)': 'noncommercial_long',
        'Noncommercial Positions-Short (All)': 'noncommercial_short',
        'Nonreportable Positions-Long (All)': 'retail_long',
        'Nonreportable Positions-Short (All)': 'retail_short',
        'Open Interest (All)': 'open_interest', 
    })

    cot_df['date'] = pd.to_datetime(cot_df['date'])

    # Resample tuần (cuối tuần, W-FRI) lấy dữ liệu cuối tuần để chuẩn hóa
    df_weekly = cot_df.set_index('date').resample('W-FRI').last().dropna().reset_index()

    # Tính net positions
    df_weekly['net_commercial'] = df_weekly['commercial_long'] - df_weekly['commercial_short']
    df_weekly['net_large'] = df_weekly['noncommercial_long'] - df_weekly['noncommercial_short']
    df_weekly['net_retail'] = df_weekly['retail_long'] - df_weekly['retail_short']

    # Thay 0 bằng NaN để tránh chia cho 0
    df_weekly['open_interest'] = df_weekly['open_interest'].replace(0, np.nan)

    # Chuẩn hóa net positions theo open interest
    df_weekly['adj_commercial'] = df_weekly['net_commercial'] / df_weekly['open_interest']
    df_weekly['adj_large'] = df_weekly['net_large'] / df_weekly['open_interest']
    df_weekly['adj_retail'] = df_weekly['net_retail'] / df_weekly['open_interest']

    # Hàm tính COT index (0-100) dựa trên vị trí normalized net position trong cửa sổ rolling `weeks`
    def calc_index(series):
        min_val = series.rolling(window=weeks, min_periods=1).min()
        max_val = series.rolling(window=weeks, min_periods=1).max()
        idx = 100 * (series - min_val) / (max_val - min_val)
        idx[max_val == min_val] = np.nan  # tránh chia 0
        return idx

    # Tính các chỉ số COT index cho từng nhóm
    df_weekly['cot_index_commercial'] = calc_index(df_weekly['adj_commercial'])
    df_weekly['cot_index_large'] = calc_index(df_weekly['adj_large'])
    df_weekly['cot_index_retail'] = calc_index(df_weekly['adj_retail'])

    return df_weekly
