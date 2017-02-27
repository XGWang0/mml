#!/usr/bin/python3

import http.client
import urllib.parse
import re
import json
import argparse
import sys
import copy

class ParameterParser(object):
    def __init__(self):
        self.add_args = None
        self.delete_args = None
        self.update_args = None
        self.list_args = None
        self.reserve_args = None
        self.release_args = None
        main_parser = argparse.ArgumentParser(
            prog=sys.argv[0],
            usage="MMLCLI <command> [<args>]\n"  + 
            "    add     Add resource to MML\n" +
            "    update  Update resource data\n" + 
            "    delete  Delete resource data\n" +
            "    list    Search resource data\n" +
            "    reserve Reserve special resource\n" +
            "    release Release special resource\n" + 
            "    extend  Extend duration for resource\n",
            )
        main_parser.add_argument("command", help="Sub command to be run")
        args = main_parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print(args.command)
            print('Unrecognized command')
            main_parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()
    
    def add(self):
        add_parser = argparse.ArgumentParser(
            description='Add resource to MML')
        add_parser.add_argument("-n", "--name", dest="rs_name", 
                                action="store", metavar="Resorce Name")
        add_parser.add_argument("-g", "--group", dest="g_name", default="",
                                nargs="?", action="store", metavar="Group Name")
        add_parser.add_argument("-N", "--note", dest="rs_note", default="",
                                nargs="?", action="store", metavar="Resorce Note")
        self.add_args = len(sys.argv) > 2 and add_parser.parse_args(sys.argv[2:]) 

    def update(self):
        update_parser = argparse.ArgumentParser(
            description='Update resource ')
        update_parser.add_argument("-n", "--name", dest="u_rs_name", 
                                   action="store", metavar="Resorce Name")
        update_parser.add_argument("-r", "--newname", dest="u_rs_rename", default="",
                                   nargs="?", action="store", metavar="New Resource Name")
        update_parser.add_argument("-g", "--newgroup", dest="u_g_name", default="",
                                   nargs="?", action="store", metavar="New Group Name")
        self.update_args = update_parser.parse_args(sys.argv[2:])

    def delete(self):
        remove_parser = argparse.ArgumentParser(
            description='Update resource data')
        remove_parser.add_argument("-n", "--name", dest="r_rs_name", 
                                   action="store", metavar="Resorce Name")
        remove_parser.add_argument("-s", "--status", dest="r_s_status", default="",
                                   nargs="?", action="store", metavar="Status")
        remove_parser.add_argument("-g", "--group_name", dest="r_g_name", default="",
                                   nargs="?", action="store", metavar="Group Name",
                                   help="Remove all resource within special group")
        self.delete_args = remove_parser.parse_args(sys.argv[2:])

    def list(self):
        list_parser = argparse.ArgumentParser(
            description='Search special resource data')
        list_parser.add_argument("-n", "--name", dest="s_rs_name", 
                                   nargs="?", action="store", metavar="Resorce Name",
                                   help="Search special resources thru source name")
        list_parser.add_argument("-s", "--status", dest="s_status", default="",
                                   nargs="?", action="store", metavar="Status",
                                   help="Search resource by status")
        list_parser.add_argument("-g", "--group_name", dest="s_g_name", default="",
                                   nargs="?", action="store", metavar="Group Name",
                                   help="Search resource thru group name")
        self.list_args = list_parser.parse_args(sys.argv[2:])

    def reserve(self):
        reserve_parser = argparse.ArgumentParser(
            description='Reserve resource data')
        reserve_parser.add_argument("-n", "--name", dest="l_rs_name", 
                                   action="store", metavar="Resorce Name",
                                   help="Reserve special resources thru source name")
        reserve_parser.add_argument("-d", "--duration", dest="l_s_time", metavar="Num S|M|H|D", 
                                   nargs="?",action="store")    
        self.reserve_args = reserve_parser.parse_args(sys.argv[2:])

    def release(self):
        release_parser = argparse.ArgumentParser(
            description='Reserve resource data')
        release_parser.add_argument("-n", "--name", dest="e_rs_name", 
                                   action="store", metavar="Resorce Name",
                                   help="Release special resources thru source name")
        self.release_args = release_parser.parse_args(sys.argv[2:])


class RequestOPT(object):
    def __init__(self, site='147.2.212.220', port=8080):
        self.site = site
        self.port = port
        self.con = http.client.HTTPConnection(self.site, self.port)
    
    def PostOpt(self, url, body, stype='POST'):
        body = json.dumps(body)
        headers = {}
        headers['CONTENT-TYPE'] = 'application/json'
        self.con.request(stype, url, body, headers)
        rsp = json.loads(self.con.getresponse().read().decode("utf-8"))
        print(rsp['msg'])
        if not rsp['status']:
            exit(1)
        return rsp['value']


VERSION = '1.0'
URL_BODY_MAP = {
    'add':{
        'url':'/%s/ResourceNew' %VERSION,
        'body':{
            'resource':{'name':'11m', 'note':'None'}, 
            'group'   :{'name':'Universal', 'note':'None'}, 
            'status'  :{'status':'Free', 'duration':''}
            }
        },
    'list':{
        'url':'/%s/ResourceSearch/' %VERSION,
        'body':{}
        },
    'update':{
        'url':'/%s/ResourceUpdate' %VERSION,
        'body':{
            'resource':{'name':'', 'note':'','newname':''}, 
            'group'   :{'name':'', 'note':''}, 
            'status'  :{'status':'', 'duration':''}}
        },
    'release':{
        'url':'/%s/ResourceRelease' %VERSION,
        'body':{
            'resource':{'name':'11m', 'note':'Reserved','id':1}, 
            'group'   :{'name':'apac2', 'note':'aaaa'}, 
            'status'  :{},
            },
        },
    'delete':{
        'url':'/%s/ResourceDelete/' %VERSION,
        'body':{}
        },
    }

class CombinArgsAndRestAPI(object):
    def __init__(self):
        pp = ParameterParser()
        self.add_parms = pp.add_args
        self.delete_parms = pp.delete_args
        self.update_parms = pp.update_args
        self.list_parms = pp.list_args
        self.reserve_params = pp.reserve_args
        self.release_params = pp.release_args
    
    def add_opt(self):
        if self.add_parms:
            tmp_a_data = copy.deepcopy(URL_BODY_MAP['add'])
            a_url = tmp_a_data['url']
            a_body = tmp_a_data['body']
            sr_namae = self.add_parms.rs_name
            sr_group = self.add_parms.g_name and self.add_parms.g_name or "Universal"
            sr_note = self.add_parms.rs_note and self.add_parms.rs_note or ""
            a_body['resource']['name'] = sr_namae
            a_body['group']['name'] = sr_group
            a_body['resource']['note'] = sr_note
            RequestOPT().PostOpt(a_url, a_body)

    def update_opt(self):
        if self.update_parms:
            tmp_a_data = copy.deepcopy(URL_BODY_MAP['update'])
            u_url = tmp_a_data['url']
            u_body = tmp_a_data['body']
            sr_namae = self.update_parms.u_rs_name
            sr_newname = self.update_parms.u_rs_rename and self.update_parms.u_rs_rename or ""
            sr_group = self.update_parms.u_g_name and self.update_parms.u_g_name or ""

            u_body['resource']['name'] = sr_namae
            u_body['resource']['newname'] = sr_newname
            u_body['group']['name'] = sr_group
            u_body['resource']['note'] = sr_group
            RequestOPT().PostOpt(u_url, u_body)

    def list_opt(self):
        if self.list_parms:
            tmp_l_data = copy.deepcopy(URL_BODY_MAP['list'])
            l_url = tmp_l_data['url']
            l_body = tmp_l_data['body']
            sr_name = self.list_parms.s_rs_name and self.list_parms.s_rs_name or None
            sr_status = self.list_parms.s_status and self.list_parms.s_status or None
            sr_group = self.list_parms.s_g_name and self.list_parms.s_g_name or None
            url_list = []
            if sr_name:
                url_list.append('name=%s' %sr_name)
            if sr_group:
                url_list.append('group=%s' %sr_group)
            if sr_status:
                url_list.append('status=%s' %sr_status)
            if url_list:
                l_url = l_url + '&'.join(url_list)
            else:
                l_url = l_url + 'ALL'
            rel = RequestOPT().PostOpt(l_url, l_body, 'GET')
            format = "{0[0]:<4} {0[1]:^10} {0[2]:^10} {0[3]:^8} {0[4]:^20} {0[5]:^20}"
            if rel:
                print(format.format(['ID', 'Name', 'G Name', 'Status', 'S StartTime', 'S EndTime']))
            for j in rel:
                rel = list(map(lambda i: str(i), j))
                print(format.format(rel))
            not rel and print("[INFO ]:No data found")

    def remove_opt(self):
        if self.delete_parms:
            tmp_a_data = copy.deepcopy(URL_BODY_MAP['delete'])
            l_url = tmp_a_data['url']
            l_body = tmp_a_data['body']
            sr_name = self.delete_parms.r_rs_name
            sr_status = self.delete_parms.r_g_name and self.delete_parms.r_g_name or None
            sr_group = self.delete_parms.r_s_status and self.delete_parms.r_s_status or None
            url_list = []
            if sr_name:
                url_list.append('name=%s' %sr_name)
            if sr_group:
                url_list.append('group=%s' %sr_group)
            if sr_status:
                url_list.append('status=%s' %sr_status)
            l_url = l_url + '&'.join(url_list)
            RequestOPT().PostOpt(l_url, l_body)


    def reserve_opt(self):
        if self.reserve_params:
            tmp_a_data = copy.deepcopy(URL_BODY_MAP['update'])
            u_url = tmp_a_data['url']
            u_body = tmp_a_data['body']
            sr_name = self.reserve_params.l_rs_name
            sr_duration = self.reserve_params.l_s_time

            u_body['resource']['name'] = sr_name
            u_body['status']['duration'] = sr_duration
            u_body['status']['status'] = 'Reserve'
            RequestOPT().PostOpt(u_url, u_body)

    def release_opt(self):
        if self.release_params:
            tmp_a_data = copy.deepcopy(URL_BODY_MAP['update'])
            u_url = tmp_a_data['url']
            u_body = tmp_a_data['body']
            sr_name = self.release_params.e_rs_name
            u_body['resource']['name'] = sr_name
            u_body['status']['status'] = 'Free'
            RequestOPT().PostOpt(u_url, u_body)

    def __call__(self):
        self.add_opt()
        self.update_opt()
        self.list_opt()
        self.remove_opt()
        self.reserve_opt()
        self.release_opt()

if __name__ == '__main__':
    '''
    url = "/1.0/ResourceNew"
    #body = {'duration':'30m', 'status':'Reserved'}
    body = {'resource':{'name':'11m', 'note':'Reserved'}, 'group':{'name':'apac2', 'note':'aaaa'}, 'status':{'status':'Reserved', 'duration':'30M'}}

    url = "/1.0/ResourceUpdate"
    #body = {'duration':'30m', 'status':'Reserved'}
    body = {'resource':{'name':'11m', 'note':'Reserved','id':1}, 'group':{'name':'apac2', 'note':'aaaa'}, 'status':{'status':'Reserved', 'duration':'30M'}}
    
    url = "/1.0/ResourceRelease"
    #body = {'duration':'30m', 'status':'Reserved'}
    body = {'resource':{'name':'11m', 'note':'Reserved','id':1}, 'group':{'name':'apac2', 'note':'aaaa'}, 'status':{'status':'Free', 'duration':'30M'}}

    url = "/1.0/ResourceDelete/id=1"
    #body = {'duration':'30m', 'status':'Reserved'}
    body = {}
    RequestOPT().PostOpt(url, body)
    '''
    CombinArgsAndRestAPI()()
