#! /usr/bin/env python

from datetime import datetime

def get_time():
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    old_time = datetime.strptime('2017-01-13 12:00:22.345', fmt)
    print(old_time)
    current_time = datetime.now()
    print(current_time)
    diff = current_time - old_time
    # minutesDiff = daysDiff * 24 * 60
    print(divmod(diff.total_seconds(), 60))

if __name__ == '__main__':
    get_time()
