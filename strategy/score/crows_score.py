def three_crows_score(today_kline_idx,klines):
    today = klines.iloc[today_kline_idx]
    yesterday = klines.iloc[today_kline_idx - 1]
    day_before_yesterday = klines.iloc[today_kline_idx - 2]

    today_body_size = (max(today['close'],today['open']) - min(today['close'],today['open'])) / today['open']
    yesterday_body_size = (max(yesterday['close'], yesterday['open']) - min(yesterday['close'], yesterday['open'])) / yesterday['open']
    day_before_yesterday_body_size = (max(day_before_yesterday['close'], day_before_yesterday['open']) - min(day_before_yesterday['close'], day_before_yesterday['open'])) / day_before_yesterday['open']

    scores = 1

    bodies = [today_body_size,yesterday_body_size,day_before_yesterday_body_size]
    for body_size in bodies:
        if 0.05 >= body_size > 0.02:
            scores += 0
        elif 0.1 >= body_size > 0.05:
            scores += 1
        elif body_size > 0.1:
            scores += 2
    return scores


