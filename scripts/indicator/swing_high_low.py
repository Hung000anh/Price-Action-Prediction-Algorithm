#./indicator/swing_high_low.py
import numpy as np

def calculate_swing_high_low(df, timeframe='D'):
    """
    Tính swing high/low và lọc đỉnh/đáy hợp lệ theo logic đã cho.
    Trả về df với 2 cột mới: 'valid_swing_high', 'valid_swing_low' (bool).
    """
    df = df.reset_index(drop=True)

    if(timeframe == 'D'):
        window = 5
    elif(timeframe == 'W'):
        window = 4
    elif(timeframe == 'M'):
        window = 3
    else:
        raise ValueError("Invalid timeframe")
    highs = df['high']
    lows = df['low']

    swing_highs = []
    swing_lows = []
    n = len(df)

    # Tìm điểm swing high/low thô
    for i in range(n):
        start = max(i - window, 0)
        end = min(i + window + 1, n)

        max_around = highs[start:i].max() if i > start else -np.inf
        max_around = max(max_around, highs[i+1:end].max() if i+1 < end else -np.inf)

        min_around = lows[start:i].min() if i > start else np.inf
        min_around = min(min_around, lows[i+1:end].min() if i+1 < end else np.inf)

        swing_highs.append(highs[i] > max_around)
        swing_lows.append(lows[i] < min_around)

    df['swing_high'] = swing_highs
    df['swing_low'] = swing_lows

    swing_high_indices = df.index[df['swing_high']].tolist()
    swing_low_indices = df.index[df['swing_low']].tolist()

    # Hàm kiểm tra swing high hợp lệ
    def is_valid_swing_high(sh_idx):
        lows_before = [idx for idx in swing_low_indices if idx < sh_idx]
        lows_after = [idx for idx in swing_low_indices if idx > sh_idx]
        if not lows_before or not lows_after:
            return False
        low_before_idx = max(lows_before)
        low_after_idx = min(lows_after)
        high_price = df.at[sh_idx, 'high']
        low_before_price = df.at[low_before_idx, 'low']
        low_after_price = df.at[low_after_idx, 'low']
        return low_before_price < high_price and low_after_price < high_price

    # Hàm kiểm tra swing low hợp lệ
    def is_valid_swing_low(sl_idx):
        highs_before = [idx for idx in swing_high_indices if idx < sl_idx]
        highs_after = [idx for idx in swing_high_indices if idx > sl_idx]
        if not highs_before or not highs_after:
            return False
        high_before_idx = max(highs_before)
        high_after_idx = min(highs_after)
        low_price = df.at[sl_idx, 'low']
        high_before_price = df.at[high_before_idx, 'high']
        high_after_price = df.at[high_after_idx, 'high']
        return high_before_price > low_price and high_after_price > low_price

    valid_swing_highs = [(idx, is_valid_swing_high(idx)) for idx in swing_high_indices]
    valid_swing_lows = [(idx, is_valid_swing_low(idx)) for idx in swing_low_indices]

    df['valid_swing_high'] = False
    for idx, valid in valid_swing_highs:
        df.at[idx, 'valid_swing_high'] = valid

    df['valid_swing_low'] = False
    for idx, valid in valid_swing_lows:
        df.at[idx, 'valid_swing_low'] = valid

    # Lọc loại bỏ các đỉnh liên tiếp không hợp lệ
    def filter_consecutive_highs():
        valid_highs = df.index[df['valid_swing_high']].tolist()
        valid_lows = df.index[df['valid_swing_low']].tolist()
        filtered_highs = []

        i = 0
        while i < len(valid_highs):
            curr_high = valid_highs[i]

            if i == len(valid_highs) - 1:
                filtered_highs.append(curr_high)
                break

            next_high = valid_highs[i + 1]
            lows_between = [low for low in valid_lows if curr_high < low < next_high]

            if lows_between:
                filtered_highs.append(curr_high)
                i += 1
            else:
                curr_high_price = df.at[curr_high, 'high']
                next_high_price = df.at[next_high, 'high']

                if curr_high_price > next_high_price:
                    filtered_highs.append(curr_high)
                    i += 2  # bỏ next_high
                else:
                    i += 1  # bỏ curr_high, giữ next_high

        if valid_highs[-1] not in filtered_highs:
            filtered_highs.append(valid_highs[-1])

        df['valid_swing_high'] = False
        df.loc[filtered_highs, 'valid_swing_high'] = True

    # Lọc loại bỏ các đáy liên tiếp không hợp lệ
    def filter_consecutive_lows():
        valid_lows = df.index[df['valid_swing_low']].tolist()
        valid_highs = df.index[df['valid_swing_high']].tolist()
        filtered_lows = []

        i = 0
        while i < len(valid_lows):
            curr_low = valid_lows[i]

            if i == len(valid_lows) - 1:
                filtered_lows.append(curr_low)
                break

            next_low = valid_lows[i + 1]
            highs_between = [high for high in valid_highs if curr_low < high < next_low]

            if highs_between:
                filtered_lows.append(curr_low)
                i += 1
            else:
                curr_low_price = df.at[curr_low, 'low']
                next_low_price = df.at[next_low, 'low']

                if curr_low_price < next_low_price:
                    filtered_lows.append(curr_low)
                    i += 2  # bỏ next_low
                else:
                    i += 1  # bỏ curr_low, giữ next_low

        if valid_lows[-1] not in filtered_lows:
            filtered_lows.append(valid_lows[-1])

        df['valid_swing_low'] = False
        df.loc[filtered_lows, 'valid_swing_low'] = True

    filter_consecutive_highs()
    filter_consecutive_lows()

    return df