
import pandas as pd
from technical.swing_points import swing_high_low

def get_structure_trend(df, timeframe):
    df = swing_high_low(df, timeframe)
    df['time'] = pd.to_datetime(df['time'])

    valid_highs = df[df['valid_swing_high']].reset_index(drop=True)
    valid_lows = df[df['valid_swing_low']].reset_index(drop=True)
    
    recent_highs = valid_highs.tail(2).reset_index(drop=True)
    recent_lows = valid_lows.tail(2).reset_index(drop=True)

    if len(recent_highs) < 2 or len(recent_lows) < 2:
        return "Indeterminate"

    highs_increasing = recent_highs.loc[1, 'high'] > recent_highs.loc[0, 'high']
    lows_increasing = recent_lows.loc[1, 'low'] > recent_lows.loc[0, 'low']

    highs_decreasing = recent_highs.loc[1, 'high'] < recent_highs.loc[0, 'high']
    lows_decreasing = recent_lows.loc[1, 'low'] < recent_lows.loc[0, 'low']

    if highs_increasing and lows_increasing:
        trend = 'Uptrend'
    elif highs_decreasing and lows_decreasing:
        trend = 'Downtrend'
    else:
        trend = 'Divergence'

    high_str = (
        f"Highs: \n{recent_highs.loc[0, 'time'].date()}:{recent_highs.loc[0, 'high']:.5f}, \n"
        f"{recent_highs.loc[1, 'time'].date()}:{recent_highs.loc[1, 'high']:.5f}"
    )
    low_str = (
        f"Lows:  \n{recent_lows.loc[0, 'time'].date()}:{recent_lows.loc[0, 'low']:.5f}, \n"
        f"{recent_lows.loc[1, 'time'].date()}:{recent_lows.loc[1, 'low']:.5f}"
    )

    return f"{trend}\n{high_str}\n{low_str}"