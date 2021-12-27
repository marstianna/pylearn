import datetime


def filter_today(results):
    return filter_day(results, datetime.datetime.now().strftime('%Y-%m-%d'))


def filter_day(results, day):
    new_results = []
    day = day + " 00:00:00";
    for result in results:
        if result['date'] == day:
            new_results.append(result)
    return new_results

def filter_last_day(results):
    return [results[len(results)-1]]
