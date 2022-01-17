import days_constant
from result import Result
import talib as ta


# TODO 星型图是由三个蜡烛图组成
from strategy.score import star_score


def morning_star(klines):
    days = days_constant.day_5
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        if (index + 1) >= len(klines):
            continue
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]
        tomorrow = klines.iloc[index + 1]

        # 昨天必须是绿色
        if yesterday['close'] > yesterday['open']:
            continue
        # 明天必须是红色
        if tomorrow['close'] < tomorrow['open']:
            continue

        if max(today['open'], today['close']) > min(yesterday['open'], yesterday['close']):
            continue

        if min(tomorrow['open'], tomorrow['close']) < max(today['open'], today['close']):
            continue

        if tomorrow['close'] > 0.5 * (yesterday['open'] + yesterday['close']):
            satisfy_ma = True
            # 连续days天ma趋势线都是下跌形态
            for ma_index in range(days):
                if ma_index == 0:
                    continue
                satisfy_ma = ma[index - ma_index] < ma[index - ma_index - 1]
                if not satisfy_ma:
                    break
            if satisfy_ma:
                satisfy_low = True
                for body_index in range(days):
                    if body_index == 0:
                        continue
                    satisfy_low = today['open'] < min(klines.iloc[index - body_index]['close'],
                                                      klines.iloc[index - body_index]['open'])
                    if not satisfy_low:
                        break
                if satisfy_low:
                    score = star_score.morning_star_score(index, klines)
                    results.append(
                        Result(today['code'], 'BUY', today['close'], today['time_key'], 'morning_star',intension=score))
    return results


def evening_star(klines):
    days = days_constant.day_5
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        if (index + 1) >= len(klines):
            continue
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]
        tomorrow = klines.iloc[index + 1]

        # 昨天必须是红色
        if yesterday['close'] < yesterday['open']:
            continue
        # 明天必须是绿色
        if tomorrow['close'] > tomorrow['open']:
            continue

        # if tomorrow['volume'] < yesterday['volume']:
        #     continue

        if min(today['open'], today['close']) < max(yesterday['open'], yesterday['close']):
            continue

        # if max(tomorrow['open'],tomorrow['close']) > min(today['open'],today['close']):
        #     continue

        if tomorrow['close'] < 0.5 * (yesterday['open'] + yesterday['close']):

            satisfy_ma = True
            # 连续days天ma趋势线都是上涨形态
            for ma_index in range(days):
                if ma_index == 0:
                    continue
                satisfy_ma = ma[index - ma_index] > ma[index - ma_index - 1]
                if not satisfy_ma:
                    break;
            if satisfy_ma:
                satisfy_high = True;
                for body_index in range(days):
                    if body_index == 0:
                        continue
                    satisfy_high = today['open'] > max(klines.iloc[index - body_index]['close'],
                                                       klines.iloc[index - body_index]['open'])
                    if not satisfy_high:
                        break;
                if satisfy_high:
                    scores = star_score.evening_star_score(index,klines)
                    results.append(
                        Result(today['code'], 'SELL', today['close'], today['time_key'], 'evening_star',intension=scores))

    return results


def falling_star(klines, k=3):
    results = []
    for index in range(len(klines)):
        if index < 1:
            continue
        if (index + 1) >= len(klines):
            continue;
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]
        tomorrow = klines.iloc[index + 1]

        today_upper_line = today['high'] - max(today['open'], today['close'])
        yesterday_upper_line = yesterday['high'] - max(yesterday['open'], yesterday['close'])
        tomorrow_upper_line = tomorrow['high'] - max(tomorrow['open'], tomorrow['close'])

        today_lower_line = min(today['open'], today['close']) - today['low']
        yesterday_lower_line = min(yesterday['open'], yesterday['close']) - yesterday['low']
        tomorrow_lower_line = min(tomorrow['open'], tomorrow['close']) - tomorrow['low']

        today_body = max(today['open'], today['close']) - min(today['open'], today['close'])
        yesterday_body = max(yesterday['open'], yesterday['close']) - min(yesterday['open'], yesterday['close'])
        tomorrow_body = max(tomorrow['open'], tomorrow['close']) - min(tomorrow['open'], tomorrow['close'])

        if today_lower_line * k > today_upper_line:
            continue
        if yesterday_lower_line * k > yesterday_upper_line:
            continue
        if tomorrow_lower_line * k > tomorrow_upper_line:
            continue
        if today_upper_line < today_body:
            continue
        if yesterday_upper_line < yesterday_body:
            continue
        if tomorrow_upper_line < tomorrow_body:
            continue
        results.append(
            Result(today['code'], 'SELL', today['close'], today['time_key'], 'falling_star'))
    return results
