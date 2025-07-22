def moving_averages(df, windows=[30, 60, 90]):
    for w in windows:
        df[f'MA{w}'] = df['close'].rolling(window=w).mean()
    return df