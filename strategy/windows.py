import constant
from result import Result
from strategy.score import window_score


def lower_broken_windows(klines,windows):
    results = []
    if len(windows) == 0:
        return results
    pass


def upper_broken_windows(klines,windows):
    results = []
    if len(windows) == 0:
        return results
    for idx in range(len(klines)):
        today = klines.iloc[idx]
        for window in windows:
            if window.date == today['time_key']:
                pass
    pass


def upper_windows(klines):
    results = []
    return results


def lower_windows(klines):
    results = []

    for index in range(len(klines)):
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]

        if today['high'] < yesterday['low']:
            keep_window = True
            for idx in range(constant.day_12):
                index_idx = index + idx
                if index_idx >= len(klines):
                    continue
                kline = klines.iloc[index_idx]
                if max(kline['open'],kline['close']) > today['high']:
                    keep_window = False
                    break
            if keep_window:
                scores = window_score.lower_window_score(index, klines)
                results.append(
                    Result(today['code'], 'SELL', today['high'], today['time_key'], 'lower_window',
                           intension=scores))
    return results
