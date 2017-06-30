from apscheduler.schedulers.blocking import BlockingScheduler
from SQLlighter import SQLlighter
import os
import re
import requests
import filecmp
import config

def sched():
    schedule = BlockingScheduler()
    @schedule.scheduled_job('cron', hour=4)
    def scheduled_job():
        groups = []
        [groups.append(date) for file in os.listdir('./schedules') for date in re.findall(r"\d+", file)]

        for group in groups:
            response = requests.get('http://www.sgu.ru/schedule/knt/do/{}/lesson'.format(group))
            with open('schedules/temp.xls', 'wb') as output:
                output.write(response.content)
            if not filecmp.cmp('./schedules/schedule{}.xls'.format(group), './schedules/temp.xls'):
                with open('./schedules/schedule{}.xls'.format(group), 'wb') as output:
                    output.write(response.content)
                s = SQLlighter(config.database_name)
                s.update_schedule_by_group(group)
        os.remove('./schedules/temp.xls')
    try:
        schedule.start()
    except (KeyboardInterrupt, SystemExit):
        pass