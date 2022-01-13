
#1.昨天的实体越大越好 2.今天的实体越小越好 3.明天的实体刺透昨天的实体越多越好,swallow最好 4.明天的成交量越大越好
def morning_star_score(today_kline_idx,klines):
    today = klines.iloc[today_kline_idx]
    today_max = max(today['close'], today['open'])
    today_min = min(today['close'], today['open'])
    today_body = today_max - today_min

    yesterday = klines.iloc[today_kline_idx - 1]
    yesterday_max = max(yesterday['close'], yesterday['open'])
    yesterday_min = min(yesterday['close'], yesterday['open'])
    yesterday_body = yesterday_max - yesterday_min

    tomorrow = klines.iloc[today_kline_idx - 1]
    tomorrow_max = max(tomorrow['close'], tomorrow['open'])
    tomorrow_min = min(tomorrow['close'], tomorrow['open'])
    tomorrow_body = tomorrow_max - tomorrow_min

    scores = 3

    # 今天的实体越小越好
    today_low = min(today['open'], today['close'])
    today_body_size = today_body / today_low
    if 0.03 >= today_body_size >= 0.01:
        scores += 1
    elif 0.01 > today_body_size >= 0:
        scores += 2


    # 昨天的实体越大越好
    yesterday_body_size = yesterday_body / yesterday_min
    if 1.03 <= yesterday_body_size <= 1.05:
        scores += 0.5
    elif 1.05 < yesterday_body_size <= 1.1:
        scores += 1
    elif yesterday_body_size > 1.1:
        scores += 1.5

    # 明天的实体刺透昨天的实体越多越好,swallow最好
    if tomorrow_max > yesterday_max:
        if tomorrow_min <= yesterday_min:
            scores += 3
        else:
            scores += 1
    else:
        if tomorrow_max > yesterday_min:
            if tomorrow_min >= yesterday_min:
                impale_body_size = tomorrow_body / yesterday_body
                if 0.5 <= impale_body_size <= 0.7:
                    scores += 1
                elif 0.7 < impale_body_size < 1:
                    scores += 2
            else:
                impale_body_size = (tomorrow_max - yesterday_min) / yesterday_body
                if 0.5 <= impale_body_size <= 0.7:
                    scores += 1
                elif 0.7 < impale_body_size < 1:
                    scores += 2
    return scores


def evening_star_score(today_kline_idx,klines):
    today = klines.iloc[today_kline_idx]
    today_max = max(today['close'], today['open'])
    today_min = min(today['close'], today['open'])
    today_body = today_max - today_min

    yesterday = klines.iloc[today_kline_idx - 1]
    yesterday_max = max(yesterday['close'], yesterday['open'])
    yesterday_min = min(yesterday['close'], yesterday['open'])
    yesterday_body = yesterday_max - yesterday_min

    tomorrow = klines.iloc[today_kline_idx - 1]
    tomorrow_max = max(tomorrow['close'], tomorrow['open'])
    tomorrow_min = min(tomorrow['close'], tomorrow['open'])
    tomorrow_body = tomorrow_max - tomorrow_min

    scores = 3

    # 今天的实体越小越好
    today_low = min(today['open'], today['close'])
    today_body_size = today_body / today_low
    if 0.03 >= today_body_size >= 0.01:
        scores += 1
    elif 0.01 > today_body_size >= 0:
        scores += 2

    # 昨天的实体越大越好
    yesterday_body_size = yesterday_body / yesterday_min
    if 1.03 <= yesterday_body_size <= 1.05:
        scores += 0.5
    elif 1.05 < yesterday_body_size <= 1.1:
        scores += 1
    elif yesterday_body_size > 1.1:
        scores += 1.5

    # 明天的实体刺透昨天的实体越多越好,swallow最好
    if tomorrow_min < yesterday_min:
        if tomorrow_max >= yesterday_max:
            scores += 3
        else:
            scores += 1
    else:
        if tomorrow_min < yesterday_max:
            if tomorrow_max <= yesterday_max:
                impale_body_size = tomorrow_body / yesterday_body
                if 0.5 <= impale_body_size <= 0.7:
                    scores += 1
                elif 0.7 < impale_body_size < 1:
                    scores += 2
            else:
                impale_body_size = (yesterday_max - tomorrow_min) / yesterday_body
                if 0.5 <= impale_body_size <= 0.7:
                    scores += 1
                elif 0.7 < impale_body_size < 1:
                    scores += 2
    return scores


def falling_star_score(today_kline_idx,klines):
    pass