import talib as ta


def calculate_press_line(today_result, klines, _timeperiod):
    hv = ta.MA(klines['high'], timeperiod=_timeperiod)
    lv = ta.MA(klines['low'], timeperiod=_timeperiod)
    today_kline = find_today_kline(today_result, klines)
    typ = (today_kline['high'] + today_kline['low'] + today_kline['close']) / 3

    for k_idx in range(len(klines)):
        if klines.iloc[k_idx]['time_key'] == today_result['date']:
            weak_press = typ * 2 - lv[k_idx]
            mid_press = typ + hv[k_idx] - lv[k_idx]
            strong_press = hv[k_idx] * 2 - lv[k_idx]
            return min(weak_press, mid_press, strong_press)


def find_today_kline(today_result, klines):
    for k_idx in range(len(klines)):
        if klines.iloc[k_idx]['time_key'] == today_result['date']:
            return klines.iloc[k_idx]
    return None


def calculate_support_line(today_result, klines, _timeperiod):
    hv = ta.MA(klines['high'], timeperiod=_timeperiod)
    lv = ta.MA(klines['low'], timeperiod=_timeperiod)
    today_kline = find_today_kline(today_result, klines)
    typ = (today_kline['high'] + today_kline['low'] + today_kline['close']) / 3

    for k_idx in range(len(klines)):
        if klines.iloc[k_idx]['time_key'] == today_result['date']:
            weak_support = typ * 2 - hv[k_idx]
            mid_support = typ - hv[k_idx] + lv[k_idx]
            strong_support = 2 * lv[k_idx] - hv[k_idx]
            return max(weak_support, mid_support, strong_support)
