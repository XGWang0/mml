import re
import json
import bottle
from db_opt.mysqlite import *
from db_opt import status_opt
from db_opt import group_opt


rq,rs = bottle.request, bottle.response


class ResourceOPT(object):
    def __init__(self):
        pass
    
    @classmethod  
    def searchResource(cls,srcname):
        sql_prefix = ("select r.id, r.name, g.name, s.status, s.start_time, " + 
                        "s.end_time from t_resource r, t_group g, t_status s where" + 
                        " r.id = g.id and r.id = s.id ")
        if re.search("^ALL$", srcname, re.I):
            sql = sql_prefix
        else:
            sql_subfix = ""
            condition = dict([i.split("=") for i in srcname.split("&")])
            if 'name' in condition:
                sql_subfix = "AND r.name = '%s'" %condition['name']
            if 'group' in condition:
                sql_subfix = sql_subfix + "AND g.name = '%s'" %condition['group']
            if 'status' in condition:
                sql_subfix = sql_subfix + "AND s.status = '%s'" %condition['status']
            sql = sql_prefix + sql_subfix
        return {'value':SQLOPT().SearchMutlTable(sql)[1], 'status':True, 'msg':''}

    @classmethod
    def getResourceID(cls, srcname):
        obj = ['id']
        rel = SQLOPT().searchTable('t_resource', obj, {'name':srcname.strip()})
        if rel['status'] and rel['value']:
            return int(rel['value'][0][0])
        else:
            return None

    @classmethod
    def newResource(cls):
        def concat(objs, data):
            mapvalues = {}
            for obj in objs:
                if (obj in data) and data[obj]:
                    mapvalues[obj] = data[obj]
            return mapvalues
    
        rq_data = json.loads(rq._get_body_string().decode("utf-8"))
        
        resource_obj = ['name', 'note']
        resrouce_values = concat(resource_obj, rq_data['resource'])
        print(rq_data,resrouce_values)
        r_ret = SQLOPT().InsertTable("t_resource", resrouce_values)
        if r_ret['status']:
            r_id = r_ret['value']
        else:
            return r_ret

        group_name = 'name' in rq_data['group'] and rq_data['group']['name'] or ""
        group_note = 'note' in rq_data['group'] and rq_data['group']['note'] or ""
        g_ret = group_opt.GroupOPT.insertGroup(r_id, group_name, group_note)
        if g_ret['status'] is False:
            return g_ret

        status_data = rq_data['status']
        curr_status = 'status' in status_data and status_data['status'] or ""
        #print('-----------',curr_status)
        duration = status_data['duration']
        s_ret = status_opt.StatusOPT.insertStatus(r_id, curr_status, duration)
        if s_ret['status'] is False:
            return s_ret

        return {'value':r_id, 'status':True, 
                'msg':'[INFO ]: Successfully add resource[%s], id:%d' %(resrouce_values['name'],
                                                                        int(r_id))}

    @classmethod
    def updateResource(cls):
        rq_data = json.loads(rq._get_body_string().decode("utf-8"))
        print(rq_data)
        resource_data = rq_data['resource']
       
        r_id = None
        r_data = rq_data['resource']
        if 'name' in r_data:
            r_id = cls.getResourceID(r_data['name'])          
        if r_id:
            if 'newname' in r_data and r_data['newname']:
                rel = SQLOPT().UpdateTable("t_resource", {'name':r_data['newname']}, {'id':r_id})
                if not rel['status']:
                    return rel
        else:
            return {'value':'', 'status':False, 'msg':'[WARN ]: No row found for resource name [%s]' %r_data['name']}

        if 'group' in rq_data and rq_data['group']:
            group_data = rq_data['group']
            group_name = 'name' in group_data and group_data['name'] or ""
            group_note = 'note' in group_data and group_data['note'] or ""
            if group_name or group_note:
                g_ret = group_opt.GroupOPT.updateGroup(r_id, group_name, group_note)
                if g_ret['status'] is False:
                    return  g_ret

        if 'status' in rq_data: 
            status_data = rq_data['status']
            curr_status = 'status' in status_data and status_data['status'] or ""
            if re.search('Reserve', curr_status, re.I):
                if status_opt.StatusOPT.searchStatus(r_id):
                    return {'value':r_id, 'status':False,
                            'msg':'[WARN ]: The resource[%s] has been reserved already' %r_data['name']}
            print('--------',curr_status)
            if re.search("free", curr_status, re.I):
                duration = ""
            else:
                duration = status_data['duration']
            s_ret = status_opt.StatusOPT.updateStatus(r_id, curr_status, duration)
            if s_ret is False:
                return  s_ret
        return  {'value':r_id, 'status':True, 'msg':'[INFO ]: Successfully update resource'}
    
    @classmethod
    def deleteResource(cls, srcname):
        print(srcname)
        condition = dict([srcname.split('=')])
        rel = SQLOPT().deleteTable('t_resource', condition)

        return {'value':rel, 'status':True, 'msg':'Successfully delete resource [%s]' %srcname.split('=')[1]}

if __name__ == '__main__':
    print(ResourceOPT.searchResource('s1'))