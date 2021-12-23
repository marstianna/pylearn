import datetime

def filter_today(results):
    new_results = []
    for result in results:
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        now = now + " 00:00:00";
        if result['date'] == now:
            new_results.append(result)
    return new_results