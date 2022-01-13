# hammer评分为3个纬度:1.实体越小,分越高 2.下影线越长,分越高 3.上影线越短越好

def hammer_score(today_kline_idx, klines):
    today = klines.iloc[today_kline_idx]

    today_upper_line = today['high'] - max(today['open'], today['close'])
    today_lower_line = min(today['open'], today['close']) - today['low']
    today_body = max(today['open'], today['close']) - min(today['open'], today['close'])
    today_low = min(today['open'], today['close'])
    scores = 0

    lower_line_size = today_lower_line / today_low
    if 0.03 <= lower_line_size <= 0.05:
        scores += 1
    elif 0.05 < lower_line_size <= 0.1:
        scores += 2
    elif lower_line_size > 0.1:
        scores += 3

    today_body_size = today_body / today_low
    if 0.03 >= today_body_size >= 0.01:
        scores += 1
    elif 0.01 > today_body_size >= 0:
        scores += 2

    upper_line_size = today_upper_line / today_low
    if 0.03 >= upper_line_size >= 0.01:
        scores += 1
    elif 0.01 > upper_line_size >= 0:
        scores += 2

    return scores


# 跟hammer评分相反:1.上影线越长越高 2.下影线越短越高 3.实体越小越高
def handstand_hammer_score(today_kline_idx, klines):
    today = klines.iloc[today_kline_idx]

    today_upper_line = today['high'] - max(today['open'], today['close'])
    today_lower_line = min(today['open'], today['close']) - today['low']
    today_body = max(today['open'], today['close']) - min(today['open'], today['close'])
    today_low = min(today['open'], today['close'])
    scores = 0

    lower_line_size = today_lower_line / today_low
    if 0.03 >= lower_line_size >= 0.01:
        scores += 1
    elif 0.01 > lower_line_size >= 0:
        scores += 2

    today_body_size = today_body / today_low
    if 0.03 >= today_body_size >= 0.01:
        scores += 1
    elif 0.01 > today_body_size >= 0:
        scores += 2

    upper_line_size = today_upper_line / today_low
    if 0.03 <= upper_line_size <= 0.05:
        scores += 1
    elif 0.05 < upper_line_size <= 0.1:
        scores += 2
    elif upper_line_size > 0.1:
        scores += 3

    return scores
