# 1.实体越长,分越高 2.成交量越大,分越高 3.today[open] - yesterday[close]越大分越高
def lower_belt_hold_line_score(today_kline_idx,klines):
    today = klines.iloc[today_kline_idx]
    yesterday = klines.iloc[today_kline_idx - 1]

    scores = 2

    today_body_size = (max(today['close'],today['open']) - min(today['close'],today['open'])) / yesterday['close']

    if 0.03 <= today_body_size < 0.05:
        scores += 1
    elif 0.05<= today_body_size < 0.1:
        scores += 2
    elif today_body_size >= 0.1:
        scores += 3

    diff = (today['open'] - yesterday['close'])/yesterday['close']
    if 0.03 <= diff < 0.05:
        scores += 1
    elif 0.05 <= diff <= 0.1:
        scores += 2

    volumes = 0
    for i in range(1, 11):
        kline = klines.iloc[today_kline_idx - i]
        volumes += kline['volume']

    volume_avg = volumes / 10
    volume_size = today['volume'] / volume_avg
    if 1.3 <= volume_size <= 1.5:
        scores += 1
    elif volume_size > 1.5:
        scores += 2
    return scores


def upper_belt_hold_line_score(today_kline_idx,klines):
    today = klines.iloc[today_kline_idx]
    yesterday = klines.iloc[today_kline_idx - 1]

    scores = 2

    today_body_size = (max(today['close'],today['open']) - min(today['close'],today['open'])) / yesterday['close']

    if 0.03 <= today_body_size < 0.05:
        scores += 1
    elif 0.05<= today_body_size < 0.1:
        scores += 2
    elif today_body_size >= 0.1:
        scores += 3

    diff = (yesterday['close'] - today['open'])/yesterday['close']
    if 0.03 <= diff < 0.05:
        scores += 1
    elif 0.05 <= diff <= 0.1:
        scores += 2

    volumes = 0
    for i in range(1, 11):
        kline = klines.iloc[today_kline_idx - i]
        volumes += kline['volume']

    volume_avg = volumes / 10
    volume_size = today['volume'] / volume_avg
    if 1.3 <= volume_size <= 1.5:
        scores += 1
    elif volume_size > 1.5:
        scores += 2
    return scores