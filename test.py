import argparse
import sys


class ParameterParser(object):
    def __init__(self):
        self.add_args = None
        self.remove_args = None
        self.update_args = None
        self.search_args = None
        self.reserve_args = None
        self.release_args = None
        main_parser = argparse.ArgumentParser(
            prog=sys.argv[0],
            usage="MMLCLI <command> [<args>]\n"  + 
            "    add     Add resource to MML\n" +
            "    update  Update resource data\n" + 
            "    delete  Delete resource data\n" +
            "    search  Search resource data\n" +
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
                                nargs=1, action="store", metavar="Resorce Name")
        add_parser.add_argument("-g", "--group", dest="g_name", default="",
                                nargs="?", action="store", metavar="Group Name")
        add_parser.add_argument("-N", "--note", dest="rs_note", default="",
                                nargs="?", action="store", metavar="Resorce Note")
        self.add_args = add_parser.parse_args(sys.argv[2:])

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

    def remove(self):
        remove_parser = argparse.ArgumentParser(
            description='Update resource data')
        remove_parser.add_argument("-n", "--name", dest="r_rs_name", 
                                   action="store", metavar="Resorce Name")
        remove_parser.add_argument("-s", "--status", dest="r_s_status", default="",
                                   nargs="?", action="store", metavar="Stauts")
        remove_parser.add_argument("-g", "--group_name", dest="r_g_name", default="",
                                   nargs="?", action="store", metavar="Group Name",
                                   help="Remove all resource within special group")
        self.remove_args = remove_parser.parse_args(sys.argv[2:])

    def search(self):
        remove_parser = argparse.ArgumentParser(
            description='Search special resource data')
        remove_parser.add_argument("-n", "--name", dest="s_rs_name", 
                                   nargs="?", action="store", metavar="Resorce Name",
                                   help="Search special resources thru source name")
        remove_parser.add_argument("-s", "--status", dest="s_status", default="",
                                   nargs="?", action="store", metavar="Status",
                                   help="Search resource by status")
        remove_parser.add_argument("-g", "--group_name", dest="s_g_name", default="",
                                   nargs="?", action="store", metavar="Group Name",
                                   help="Search resource thru group name")
        self.remove_args = remove_parser.parse_args(sys.argv[2:])

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
        
#sys.argv = ['-h']
pp = ParameterParser()
print(pp.add_args)
print(pp.remove_args)
print(pp.update_args)
print(pp.search_args)
print(pp.reserve_args)
print(pp.release_args)