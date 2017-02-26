import re
import json
import datetime
import bottle
from db_opt.mysqlite import *

rq,rs = bottle.request, bottle.response


class GroupOPT(object):
    def __init__(self):
        pass

    @classmethod
    def  insertGroup(cls, tr_id, name, note):
        condition = {}
        condition['tr_id'] = tr_id
        if name:
            condition['name'] = name
        if note:
            condition['note'] = note
        
        return SQLOPT().InsertTable("t_group", condition)

    @classmethod  
    def updateGroup(cls, tr_id, name, note):
        newvalue = {}
        if not name and not note:
            return {'status':True, 'value':'', 'msg':'[INFO ]:Do not need to update group'}
        else:
            newvalue['name'], newvalue['note'] = name, note
        condition = {'tr_id':tr_id}
        rel = SQLOPT().UpdateTable("t_group", newvalue, condition)
        if rel['status'] is False and not rel['msg']:
            rel['msg'] = "[ERROR]: Failed to update group"
        return rel

if __name__ == '__main__':
    print(StatusOPT.updateStatus(1,1))