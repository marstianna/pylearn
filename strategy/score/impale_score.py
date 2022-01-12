# 穿透模型里面,评分包含三个部分:1.穿透的昨天的实体大小以及今天的实体大小 2.穿透的百分比 3.成交量
def upper_impale_score(today_kline_idx,klines):
    today = klines.iloc[today_kline_idx]
    today_max = max(today['close'], today['open'])
    today_min = min(today['close'], today['open'])
    today_body = today_max - today_min
    yesterday = klines.iloc[today_kline_idx - 1]
    yesterday_max = max(yesterday['close'], yesterday['open'])
    yesterday_min = min(yesterday['close'], yesterday['open'])
    yesterday_body = yesterday_max - yesterday_min
    scores = 0
