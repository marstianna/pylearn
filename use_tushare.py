import tushare as tu
import pandas as pd


if __name__ == '__main__':
    pro = tu.pro_api('8dfa55cdea0ff16bc4ed27eb0ecdbaacb557fea12df191df622f68d3')
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 10000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)
    daily = pro.us_daily(ts_code='AAPL', start_date='20201201', end_date='20211227')
    daily.sort_values('trade_date',ascending=True,inplace=True)
    print(daily)