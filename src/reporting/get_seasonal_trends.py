import pandas as pd
from technical.seassionality import seasonality_pivot_table, monthly_avg_for_periods_by_month


def get_seasonal_trends(df, threshold=0.05):
    pivot_table = seasonality_pivot_table(df, 'time', 2005, 'close')
    monthly_avgs = monthly_avg_for_periods_by_month(pivot_table)

    label_map = {
        'avg_20y': 'Last 20 Years',
        'avg_15y': 'Last 15 Years',
        'avg_10y': 'Last 10 Years',
        'avg_5y': 'Last 5 Years',
        'avg_2y': 'Last 2 Years'
    }

    data = []
    for period, value in monthly_avgs.items():
        if value is None or pd.isna(value):
            trend = 'Unknown'
        elif -threshold < value < threshold:
            trend = 'Sideways'
        elif value >= threshold:
            trend = 'Bullish'
        else:
            trend = 'Bearish'

        data.append({
            'Period': label_map.get(period, period),
            'Average % Change': value,
            'Trend': trend
        })

    return pd.DataFrame(data)