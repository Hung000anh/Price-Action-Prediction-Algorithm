import pandas as pd

def get_seasonal_trends(df):
    df = df.copy()
    df['time'] = pd.to_datetime(df['time'])
    max_year = df['time'].dt.year.max()
    last_date = df['time'].max()
    this_month = last_date.month
    df = df.sort_values('time').reset_index(drop=True)
    df['pct_change'] = df['close'].pct_change() * 100

    periods = [
        (max_year - 20, 'Last 20 Years'),
        (max_year - 15, 'Last 15 Years'),
        (max_year - 10, 'Last 10 Years'),
        (max_year - 5,  'Last 5 Years'),
        (max_year - 2,  'Last 2 Years')
    ]

    data = []

    for start_year, label in periods:
        temp_df = df[df['time'].dt.year >= start_year].copy()
        temp_df['year'] = temp_df['time'].dt.year
        temp_df['month'] = temp_df['time'].dt.month

        pivot = temp_df.pivot(index='year', columns='month', values='pct_change')
        monthly_avg = pivot.mean(axis=0)

        avg_val = monthly_avg.get(this_month, None)

        # Xác định trend
        if avg_val is None:
            trend = "Unknown"
        elif avg_val > 0.3:
            trend = "Uptrend"
        elif avg_val < -0.3:
            trend = "Downtrend"
        else:
            trend = "Sideways"

        data.append({
            'Period': label,
            'Average % Change': round(avg_val, 3) if avg_val is not None else None,
            'Trend': trend
        })

    return pd.DataFrame(data)
