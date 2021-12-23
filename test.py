import pandas as pd
import numpy as np
import futu as ft

import hammer_strategy
import impale_strategy
import star_strategy
import swallon_strategy
from result import Result


def test_hammer(klines):
    upper_result = hammer_strategy.define_upper_hammer(klines)
    print(pd.DataFrame(upper_result, columns=Result.columns))
    lower_result = hammer_strategy.define_lower_hammer(klines)
    print(pd.DataFrame(lower_result,columns=Result.columns))

def test_swallow(klines):
    upper_result = swallon_strategy.upper_swallow_lower(klines)
    print(pd.DataFrame(upper_result, columns=Result.columns))
    lower_result = swallon_strategy.lower_swallow_upper(klines)
    print(pd.DataFrame(lower_result, columns=Result.columns))


def test_impale(klines):
    upper_result = impale_strategy.upper_impale(klines)
    print(pd.DataFrame(upper_result, columns=Result.columns))
    lower_result = impale_strategy.lower_impale(klines)
    print(pd.DataFrame(lower_result, columns=Result.columns))

def test_star(klines):
    upper_result = star_strategy.morning_star(klines)
    print(pd.DataFrame(upper_result, columns=Result.columns))
    lower_result = star_strategy.evening_star(klines)
    print(pd.DataFrame(lower_result, columns=Result.columns))


if __name__ == '__main__':
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)
    quote_ctx = ft.OpenQuoteContext()  # 创建行情对象
    RET_OK, ret_frame = quote_ctx.get_user_security("自持有")
    for code in ret_frame['code']:
        RET_OK, kline_frame_table, next_page_req_key = quote_ctx.request_history_kline(code=code)
        test_star(kline_frame_table)
    quote_ctx.close()