#./indicator/moving_averages.py

def moving_averages(df, windows=[30, 60, 90]):
    """
    Tính các đường MA với list windows (mặc định 30, 60, 90).
    Trả về df với các cột MA tương ứng.
    """
    for w in windows:
        df[f'MA{w}'] = df['close'].rolling(window=w).mean()
    return df