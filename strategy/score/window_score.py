# 1.窗口越大,评分越高 2.今天实体越大,评分越高
def lower_window_score(today_kline_idx,klines):
    today = klines.iloc[today_kline_idx]
    yesterday = klines.iloc[today_kline_idx - 1]

    scores = 3

    today_body = max(today['high'],today['close']) - min(today['high'],today['close'])
    today_body_size = today_body / min(today['high'],today['close'])

    window = yesterday['low'] - today['high']
    window_size = window / yesterday['low']

    if window_size >= 0.05:
        # 窗口大于5%,直接清仓
        scores = 10000
        return scores
    elif 0.03 <= window_size < 0.05:
        scores *= 5
    else:
        scores *= 3
    return scores

