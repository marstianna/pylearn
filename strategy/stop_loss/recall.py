import datetime


def recall_buy(target_result, total_results,klines, target_recall_day):
    # 回溯的时候,找寻可以认为是翻转底的标识
    results = []
    for result_idx in range(len(total_results)):
        result = total_results[result_idx]
        if result['date'] == target_result['date']:
            for recall_idx in range(result_idx):
                recall_result = total_results[result_idx - recall_idx]
                end_time = datetime.datetime.strptime(recall_result['date'], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
                    days=target_recall_day)
                result_time = datetime.datetime.strptime(result['date'], "%Y-%m-%d %H:%M:%S")
                if end_time >= result_time and check_bottom(recall_result):
                    results.append(recall_result)
    return calculate_avg(results,klines,1)


def check_bottom(result):
    return result['action'] == 'BUY' and (result['strategy'] == 'swallow' or result['strategy'] == 'upper_impale' or result['strategy'] == 'morning_star')


def calculate_avg(results,klines,action):
    if len(results) == 0:
        return -1
    total_price = 0.0
    for k_idx in range(len(klines)):
        for result in results:
            if klines.iloc[k_idx]['time_key'] == result['date']:
                total_price += klines.iloc[k_idx]['low' if action == 1 else 'high']
    return total_price/len(results)

def recall_sell(target_result,total_results,target_recall_date):
    # 回溯的时候,找寻可以认为是反转顶的标识
    results=[]
    return calculate_avg(results)