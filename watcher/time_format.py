import time

def time_format():
    start_time = time.time()
    str_time = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime(start_time))
    
    return start_time, str_time