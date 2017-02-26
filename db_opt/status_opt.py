import re
import json
import datetime
import bottle
from db_opt.mysqlite import *

rq,rs = bottle.request, bottle.response


class StatusOPT(object):
    def __init__(self):
        pass


    @classmethod
    def convertDatetime(cls, duration):
        re_inst = re.search("(\d+)(m|s|h|d)", duration, re.I)
        if re_inst:
            duration_time = re_inst.groups()[0].strip()
            duration_units = re_inst.groups()[1].strip()
        else:
            return ('', '')
        datetime_format = "%Y-%m-%d %H:%M:%S"
        starttime = datetime.datetime.now()
        starttime_str = datetime.datetime.strftime(starttime, datetime_format)

        if duration_units and duration_units in ['m','M','Mon']:
            balancetime = datetime.timedelta(minutes=int(duration_time))
        elif duration_units and duration_units in ['d','D','days']:
            balancetime = datetime.timedelta(days=int(duration_time))
        elif duration_units and duration_units in ['h','H','hours']:
            balancetime = datetime.timedelta(hours=int(duration_time))
        else:
            balancetime = datetime.timedelta(seconds=int(duration_time))
        
        endtime = starttime + balancetime
        endtime_str = datetime.datetime.strftime(endtime, datetime_format)
        return (starttime_str, endtime_str)

    @classmethod
    def  insertStatus(cls, tr_id, status, duration):
        start_time, end_time = cls.convertDatetime(duration)
        condition = {'start_time':start_time, 'end_time':end_time}
        if tr_id:
            condition['tr_id'] = tr_id
        if status:
            condition['status'] = status
        
        return SQLOPT().InsertTable("t_status", condition)

    @classmethod  
    def updateStatus(cls, tr_id, status, duration):
        #rq_data = json.loads(rq._get_body_string().decode("utf-8"))
        #rq_data = {'duration':'30m', 'status':'Reserved'}
        start_time, end_time = cls.convertDatetime(duration)
        newvalue = {'start_time':start_time, 'end_time':end_time}
        if status:
            newvalue['status'] = status
        condition = {'tr_id':tr_id}
        rel = SQLOPT().UpdateTable("t_status", newvalue, condition)
        if rel['status'] is False and not rel['msg']:
            rel['msg'] = "[ERROR]: Failed to update status"
        return rel

    @classmethod
    def searchStatus(cls, tr_id):
        ret = SQLOPT().searchTable('t_status', ['status'], {'tr_id':tr_id})
        #print(ret)
        if ret['value']:
            if re.search('Reserve', ret['value'][0][0], re.I):
                return True
        else:
            return False

if __name__ == '__main__':
    print(StatusOPT.searchStatus(7))