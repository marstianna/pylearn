import constant
from result import Result


def break_upper(today_kline_idx,klines,scores):
    today = klines.iloc[today_kline_idx]
    bottom = today['low']
    days = constant.day_12
    for idx in range(1,days):
        if (today_kline_idx + idx) >= len(klines):
            break
        kline = klines.iloc[today_kline_idx+idx]
        if kline['close'] < bottom:
            return True,Result(kline['code'], 'SELL', kline['close'], kline['time_key'], 'break_upper',intension=scores)
    return False,None


def break_lower(today_kline_idx,klines,scores):
    today = klines.iloc[today_kline_idx]
    head = today['high']
    days = constant.day_12
    for idx in range(1, days):
        if (today_kline_idx + idx) >= len(klines):
            break
        kline = klines.iloc[today_kline_idx + idx]
        if kline['close'] > head:
            return True, Result(kline['code'], 'BUY', kline['close'], kline['time_key'], 'break_lower',
                                intension=scores)
    return False,None