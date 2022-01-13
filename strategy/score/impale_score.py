# 穿透模型里面,评分包含三个部分:1.穿透的昨天的实体大小以及今天的实体大小 2.穿透的百分比 3.成交量
def upper_impale_score(today_kline_idx, klines):
    today = klines.iloc[today_kline_idx]
    today_max = max(today['close'], today['open'])
    today_min = min(today['close'], today['open'])
    today_body = today_max - today_min
    yesterday = klines.iloc[today_kline_idx - 1]
    yesterday_max = max(yesterday['close'], yesterday['open'])
    yesterday_min = min(yesterday['close'], yesterday['open'])
    yesterday_body = yesterday_max - yesterday_min

    scores = 0
    today_body_size = today_body / today_min
    if 1.03 <= today_body_size <= 1.05:
        scores += 0.5
    elif 1.05 < today_body_size <= 1.1:
        scores += 1
    elif today_body_size > 1.1:
        scores += 1.5

    yesterday_body_size = yesterday_body / yesterday_min
    if 1.03 <= yesterday_body_size <= 1.05:
        scores += 0.5
    elif 1.05 < yesterday_body_size <= 1.1:
        scores += 1
    elif yesterday_body_size > 1.1:
        scores += 1.5

    impale_body = today_max - yesterday_min
    impale_body_size = impale_body / yesterday_body
    if 0.5 <= impale_body_size <= 0.7:
        scores += 1
    elif 0.7 < impale_body_size < 1:
        scores += 2

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


def lower_impale_score(today_kline_idx, klines):
    today = klines.iloc[today_kline_idx]
    today_max = max(today['close'], today['open'])
    today_min = min(today['close'], today['open'])
    today_body = today_max - today_min
    yesterday = klines.iloc[today_kline_idx - 1]
    yesterday_max = max(yesterday['close'], yesterday['open'])
    yesterday_min = min(yesterday['close'], yesterday['open'])
    yesterday_body = yesterday_max - yesterday_min

    scores = 0
    today_body_size = today_body / today_min
    if 1.03 <= today_body_size <= 1.05:
        scores += 0.5
    elif 1.05 < today_body_size <= 1.1:
        scores += 1
    elif today_body_size > 1.1:
        scores += 1.5

    yesterday_body_size = yesterday_body / yesterday_min
    if 1.03 <= yesterday_body_size <= 1.05:
        scores += 0.5
    elif 1.05 < yesterday_body_size <= 1.1:
        scores += 1
    elif yesterday_body_size > 1.1:
        scores += 1.5

    impale_body = yesterday_max - today_min
    impale_body_size = impale_body / yesterday_body
    if 0.5 <= impale_body_size <= 0.7:
        scores += 1
    elif 0.7 < impale_body_size < 1:
        scores += 2

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
