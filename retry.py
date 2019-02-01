import os
import schedule
import time

def restart():
    os.system('./restart.sh')

def run_forver():
    os.system('./restart.sh')
    schedule.every(20).minutes.do(restart)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run_forver()