def three_crows_score(today_kline_idx,klines):
    today = klines.iloc[today_kline_idx]
    yesterday = klines.iloc[today_kline_idx - 1]
    day_before_yesterday = klines.iloc[today_kline_idx - 2]

    scores = 1

