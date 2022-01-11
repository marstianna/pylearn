# swallow评分包含三个部分:1.自身实体大小(30%),2.吞噬的K线个数(50%),3.成交量(20%)
def swallow_score(today_kline_idx, klines):
    today = klines.iloc[today_kline_idx]
    today_max = max(today['close'], today['open'])
    today_min = min(today['close'], today['open'])
    scores = 0
    for i in range(1, 6):
        kline = klines.iloc[today_kline_idx - i]
        kline_max = max(kline['close'], kline['open'])
        kline_min = min(kline['close'], kline['open'])
        if kline_min >= today_min and kline_max <= today_max:
            scores += 1
    body_size = today_max / today_min

    if 1.01 <= body_size <= 1.03:
        scores += 1
    elif 1.03 < body_size <= 1.05:
        scores += 2
    elif body_size > 1.05:
        scores += 3

    volumes = 0
    for i in range(1, 8):
        kline = klines.iloc[today_kline_idx - i]
        volumes += kline['volume']

    volume_avg = volumes / 7
    volume_size = today['volume'] / volume_avg
    if 1.3 <= volume_size <= 1.5:
        scores += 1
    elif volume_size > 1.5:
        scores += 2
    elif 0.7 >= volume_size >= 0.5:
        scores -= 1
    elif volume_size < 0.5:
        scores -= 2

    return scores
