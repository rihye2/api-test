from apscheduler.schedulers.blocking import BlockingScheduler


scheduler = BlockingScheduler()
scheduler.add_job('', 'interval', seconds=5, args=[''])

def aggregate():
    #log file read
    #aggregate -> file save
    pass

try:
    scheduler.start()
except KeyboardInterrupt:
    pass