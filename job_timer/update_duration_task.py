from datetime import datetime, timedelta
import threading
from db_opt.mysqlite import *
#from job_timer.jobtimer import *
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
class UpDuration(object):
    def __init__(self):
        self.status_table = 't_status'
    
    def update_duration(self):
        #print('update database now ~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        curr_time = self.get_currtime()
        sql_cmd = "UPDATE %s set status='Free', 'start_time'='', 'end_time'='' where status='Reserve' and end_time <='%s'" %(self.status_table, curr_time)
        ret = SQLOPT().execSqlCMD(sql_cmd)
        return ret[0]

    def get_currtime(self):
        curr_datetime = datetime.now()
        curr_str_datetime = curr_datetime.strftime(DATE_FORMAT)
        return curr_str_datetime

    def __call__(self):
        return self.update_duration


#schd = MyTimer()
##schd.add_timer(5, 'up_duration')
#schd.test('up_duration', UpDuration()())