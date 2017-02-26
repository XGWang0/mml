import sqlite3
import re
from warnings import catch_warnings

class SQLITE(object):
    def __init__(self, db="/home/root/python_workspace/mysqlite_db/mml.db"):
        self.db = db
        self.cnx = None
        self.cursor = None
        
    def __enter__(self):
        if not self.cnx:
            self.cnx = sqlite3.connect(self.db)
        self.cursor = self.cnx.cursor()
        return self

    def __exit__(self, type, value, traceback):
        if value:
            print(type, "ttttttttttttt1111111111")
            if type is sqlite3.IntegrityError:
                if re.search('UNIQUE constraint', value, re.I):
                    print('WARN :' + 'The same resource already exists')
            else:
                raise
        self.cursor = None
        if self.cnx:
            self.cnx.close()
        self.cnx = None

class SQLOPT(object):
    def __init__(self):
        pass

    def execSqlCMD(self,cmd):
        #print("cmd----", cmd)
        with SQLITE() as slt:
            try:
                slt.cursor.execute(cmd)
            except sqlite3.IntegrityError as e:
                #print(e,'ssssssssssssssssss')
                if re.search('UNIQUE constraint failed', str(e), re.I):
                    #print('-----------------------')
                    return (False, "[WARN ]:The same resource already existed")
            slt.cnx.commit()
            rel = slt.cursor.lastrowid
            if not rel:
                rel = slt.cursor.fetchall()
            #print(rel, '=============================')
        return (True, rel)

    def SearchMutlTable(self, sql):
        return self.execSqlCMD(sql)

    def searchTabalAll(self, table, obj):
        obj_str = ','.join(obj)
        cmd = 'SELECT %s FROM %s'%(obj_str, table)
        
        return self.execSqlCMD(cmd)

    def searchTable(self, table, obj, condition, fuzzy=False):

        obj_str = ','.join(obj)
        cond_str = ""
        for key,value in condition.items():
            if cond_str:
                cond_str = cond_str + " AND %s='%s' " %(key, str(value))
            else:
                cond_str = " %s='%s' " %(key, str(value))
        cmd = 'SELECT %s FROM %s WHERE %s'%(obj_str, table, cond_str)
        #print("SELECT---:",cmd)
        result = self.execSqlCMD(cmd)
        if result[0]:
            return {'status':True, 'value':result[1], 'msg':''}
        else:
            return {'status':False, 'value':'', 'msg':'[WARN ]: No data found'}

    def InsertTable(self, table, condition):
        obj_str = ""
        cond_str = None
        for key,value in condition.items():
            if not obj_str:
                obj_str = "'%s' " %str(key)
                cond_str = "'%s' " %str(value)
            else:
                obj_str = "%s, '%s'" %(obj_str, str(key))
                cond_str = "%s, '%s'" %(cond_str, str(value))
        cmd = 'INSERT INTO %s (%s) VALUES (%s)'%(table, obj_str, cond_str)
        #print('INSERT---:',cmd)
        result = self.execSqlCMD(cmd)
        if result[0]:
            return {'status':True, 'value':result[1], 'msg':''}
        else:
            return {'status':False, 'value':'', 'msg':result[1]}

    def UpdateTable(self, table, newvalue, condition):
        setvalue_str = ""
        cond_str = None
        for key,value in newvalue.items():
            if not setvalue_str:
                setvalue_str = "%s='%s' " %(key, str(value))
            else:
                setvalue_str = "%s, %s='%s'" %(setvalue_str, str(key), str(value))

        for key,value in condition.items():
            if not cond_str:
                cond_str = "%s='%s' " %(key, str(value))
            else:
                cond_str = "%s AND %s='%s'" %(cond_str, str(key), str(value)) 
        
        cmd = 'UPDATE %s set %s where %s ' %(table, setvalue_str, cond_str)
        #print('UPDATE---:',cmd)
        result = self.execSqlCMD(cmd)
        if result[0]:
            #print(result[1],'update-------------')
            return {'status':True, 'value':result[1], 'msg':''}
        else:
            return {'status':False, 'value':'', 'msg':result[1]}

    def deleteTable(self, table, condition):

        cond_str = ""
        for key,value in condition.items():
            if cond_str:
                cond_str = cond_str + " AND %s='%s' " %(key, str(value))
            else:
                cond_str = " %s='%s' " %(key, str(value))
        cmd = 'DELETE FROM %s WHERE %s'%(table, cond_str)
        #print("DELETE---:",cmd)
        return self.execSqlCMD(cmd)

if __name__ == '__main__':
    print(SQLOPT().UpdateTable("t_status", {'start_time':'', 'end_time':''}, {'id':1}))