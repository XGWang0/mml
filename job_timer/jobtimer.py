from db_opt.mysqlite import *
from  datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import inspect
import json

from job_timer.update_duration_task import UpDuration
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class MyTimer(object):
    def __init__(self):
        self.datetime_format = DATE_FORMAT
        self.sched = BackgroundScheduler()
 
    def calculate_time(self, interval):
        start_date = datetime.now()
        start_time = start_date.strftime(self.datetime_format)
        end_datetimem = start_date + timedelta(seconds=int(interval))
        end_time = end_datetimem.strftime(self.datetime_format)
        
        return (start_time, end_time)
    
    def add_scheduler(self):
        self.remove_scheduler(self.job_name)
        start_time, end_time = self.calculate_time(self.interval)
        #print(start_time, end_time)
        SQLOPT().InsertTable('t_timer',{'name':self.job_name, 'interval':int(self.interval),
                                        'start_time':start_time, 'end_time':end_time})
    def remove_scheduler(self, job_name):
        SQLOPT().deleteTable('t_timer', {'name':job_name})
    
    def getInterval(self, job):
        ret = SQLOPT().searchTable('t_timer', ['interval'], {'name':job})
        #print('-'*10)
        if ret['value']:
            
            return ret['value'][0][0]
        else:
            return None
   
    def getEndTime(self, job):
        ret = SQLOPT().searchTable('t_timer', ['end_time'], {'name':job})
        #print('-'*10)
        if ret['value']:
            return ret['value'][0][0]
        else:
            return None

    def _getSelfName(self):
        my_name = inspect.stack()[0][3]
        return my_name

    def test(self, job_name, job):
        my_name = inspect.stack()[0][3]
        curr_time = datetime.now().strftime(self.datetime_format)
        #print(inspect.stack()[0][3])
        end_time = self.getEndTime(job_name)
        #print(curr_time, end_time, '==================')
        if curr_time > end_time:
            job()
            print(datetime.now(), "Scheduler is triggered")
            interval = self.interval
            #interval = self.getInterval(job_name)
            start_time, end_time = self.calculate_time(interval)
            SQLOPT().UpdateTable('t_timer', 
                                 {'start_time':start_time, 'end_time':end_time},
                                 {'name':job_name})
            
        else:
            #print(datetime.now(), "Not run obj")
            return
        
    def register(self, job_name, job, interval):
        self.add_scheduler()
        self.sched.add_job(self.test, 'interval', args=(job_name, job), seconds=interval)
    
    def run_scheduler(self, job_name, job, interval):
        self.job_name = job_name
        self.job = job
        self.interval = interval
        self.register(job_name, job, interval)
        self.sched.start()



#, args=('up_duration', UpDuration()())
if __name__ == '__main__':
    MyTimer().add_scheduler(3, 'test')
    MyTimer().run()