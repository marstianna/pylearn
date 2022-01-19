import talib as ta

import constant
from constant import day_5
from result import Result
from strategy.score import crows_score


def two_crows(klines):
    days = day_5
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        if (index+1) >= len(klines):
            continue;
        today = klines.iloc[index]
        yesterday = klines.iloc[index-1]
        tomorrow = klines.iloc[index + 1]

        # 昨天必须是红色
        if yesterday['close'] < yesterday['open']:
            continue
        # 明天必须是绿色
        if tomorrow['close'] > tomorrow['open']:
            continue

        # 今天必须是绿色
        if today['close'] > today['open']:
            continue

        if today['low'] > yesterday['high'] and tomorrow['open'] > today['open'] and tomorrow['close'] < today['close']:
            satisfy_ma = True
            # 连续days天ma趋势线都是上涨形态
            for ma_index in range(days):
                if ma_index == 0:
                    continue
                satisfy_ma = ma[index - ma_index] > ma[index - ma_index - 1]
                if not satisfy_ma:
                    break
            if satisfy_ma:
                results.append(
                    Result(today['code'], 'SELL', today['close'], today['time_key'], 'two_crows',intension=constant.default_scores))
    return results


def three_crows(klines):
    results = []
    for index in range(len(klines)):
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]
        day_before_yesterday = klines.iloc[index - 2]

        if today['open'] < today['close']:
            continue
        if yesterday['open'] < yesterday['close']:
            continue
        if day_before_yesterday['open'] < day_before_yesterday['close']:
            continue
        if today['open'] < yesterday['open'] < day_before_yesterday['open'] and today['close'] < yesterday['close'] < day_before_yesterday['close']:
            # 三只乌鸦一旦出现直接清仓
            scores = crows_score.three_crows_score(index,klines)
            if scores > 0:
                results.append(
                    Result(today['code'], 'SELL', today['close'], today['time_key'], 'three_crows',
                           intension=scores))
    return results