from apscheduler.schedulers.blocking import BlockingScheduler
import yaml
import os
import re

with open("config.yaml") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)


def aggregate():
    
    #log file read
    with open('/Users/hyeri/cloudai/api-test/agg_test.log', 'r') as log_file:
    # with open(os.path.join(cfg['log_save_process'], cfg['log_process_filename']), 'r') as log_file:
        total_time_pattern = re.compile(r'.+\[inference total time\]: (\d+\.\d+)')
        inference_times = []
        for log in log_file.readlines():
            log = log.strip()
            infer_total_time = total_time_pattern.match(log)
        
        if infer_total_time:
            inference_time = float(infer_total_time.group(1))
            inference_times.append(inference_time)
    
    
    mean_inference_time = sum(inference_times) / len(inference_times)
    min_inference_time = min(inference_times)
    max_inference_time = max(inference_times)
    
    # Print results
    print(f"Mean inference total time: {mean_inference_time:.2f}")
    print(f"Min inference total time: {min_inference_time:.2f}")
    print(f"Max inference total time: {max_inference_time:.2f}")
    
    #aggregate -> file save
    #file save 1. logging 2.file write


scheduler = BlockingScheduler()
scheduler.add_job(aggregate, 'interval', seconds=5)


try:
    scheduler.start()
except KeyboardInterrupt:
    scheduler.shutdown()
