# 穿透模型里面,评分包含三个部分:1.穿透的昨天的实体大小以及今天的实体大小 2.穿透的百分比 3.成交量
def impale_score(today_kline_idx,klines):
    return