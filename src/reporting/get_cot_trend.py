from technical.cot_index import cot_index

def get_cot_trend(cot_df, weeks=26, upperExtreme=80, lowerExtreme=20):
    # Tạo dataframe COT index tuần
    df_ = cot_index(cot_df, weeks)

    # Lấy tháng cuối cùng trong dữ liệu
    last_date = df_['date'].max()
    last_month = last_date.month
    last_year = last_date.year

    # Bỏ toàn bộ tuần thuộc tháng cuối cùng (vì tháng cuối chưa hoàn chỉnh)
    df_filtered = df_[(df_['date'].dt.year < last_year) | ((df_['date'].dt.year == last_year) & (df_['date'].dt.month < last_month))]

    # Lùi tuần từng bản ghi một
    for idx in range(len(df_filtered)-1, -1, -1):
        row = df_filtered.iloc[idx]
        cot_com = row['cot_index_commercial']
        cot_ret = row['cot_index_retail']

        bullish_mask = (cot_com >= upperExtreme) and (cot_ret <= lowerExtreme)
        bearish_mask = (cot_com <= lowerExtreme) and (cot_ret >= upperExtreme)

        # print(f"Kiểm tra tuần {row['date'].date()}: Commercial={cot_com:.2f}, Retail={cot_ret:.2f}")

        if bullish_mask:
            return (f"Uptrend\n"
                    f"Date: {row['date'].date()}\n"
                    f"Commercial COT Index: {cot_com:.2f}\n"
                    f"Retail COT Index: {cot_ret:.2f}")
        elif bearish_mask:
            return (f"Downtrend\n"
                    f"Date: {row['date'].date()}\n"
                    f"Commercial COT Index: {cot_com:.2f}\n"
                    f"Retail COT Index: {cot_ret:.2f}")

    print("Không tìm được xu hướng rõ ràng trong dữ liệu.")
    return None, None