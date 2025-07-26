from tabulate import tabulate
import numpy as np
import pandas as pd
from reporting.get_cot_trend import get_cot_trend
from reporting.get_ma_trend import get_ma_trend
from reporting.get_seasonal_trends import get_seasonal_trends
from reporting.get_structure_trend import get_structure_trend


def generate_summary_report(data):

    table = []
    
    for symbol, datasets in data.items():
        # MA trends
        ma_d = get_ma_trend(datasets['asset_data']['1D_data'], timeframe="D")
        ma_w = get_ma_trend(datasets['asset_data']['1W_data'], timeframe="W")
        ma_m = get_ma_trend(datasets['asset_data']['1M_data'], timeframe="M")

        # Market Structure
        ms_d = get_structure_trend(datasets['asset_data']['1D_data'], timeframe='D')
        ms_w = get_structure_trend(datasets['asset_data']['1W_data'], timeframe='W')
        ms_m = get_structure_trend(datasets['asset_data']['1M_data'], timeframe='M')

        # COT trend
        cot_status = get_cot_trend(datasets['cot_data'])

        # Seasonal values
        ss_t = get_seasonal_trends(datasets['asset_data']['1M_data'], threshold= 0.05)

        def format_seasonal(period):
            subset = ss_t.loc[ss_t['Period'] == period]
            if subset.empty:
                return "N/A"
            val = subset['Average % Change'].values[0]
            trend = subset['Trend'].values[0]
            return f"{trend}\nAvgs: {val:.3f}%"


        s_2y = format_seasonal('Last 2 Years')
        s_5y = format_seasonal('Last 5 Years')
        s_10y = format_seasonal('Last 10 Years')
        s_15y = format_seasonal('Last 15 Years')
        s_20y = format_seasonal('Last 20 Years')

        # Placeholder for Score
        score = "nan"

        # Append row to table
        table.append([
            symbol, ma_d, ma_w, ma_m, ms_d, ms_w, ms_m,
            cot_status, s_2y, s_5y, s_10y, s_15y, s_20y, score
        ])

    headers = [
        "Symbol", "MA D (30 60 90)", "MA W (30 60 90)", "MA M (30 60 90)",
        "Structure D (5)", "Structure W (4)", "Structure M (3)",
        "COT", "Seasonal 2Y", "Seasonal 5Y", "Seasonal 10Y",
        "Seasonal 15Y", "Seasonal 20Y", "Score"
    ]

    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))