# What is mml ?
Machines(Resource) management tool is used to manage or maintain machine resource.

#USAGE
* HELP
```console
linux-qlxp:/home/root/mml # ./MMLCLI -h
usage: MMLCLI <command> [<args>]
    add     Add resource to MML
    update  Update resource data
    delete  Delete resource data
    list    Search resource data
    reserve Reserve special resource
    release Release special resource
    extend  Extend duration for resource

positional arguments:
  command     Sub command to be run

optional arguments:
  -h, --help  show this help message and exit

```console

* add
```console
xgwang@linux-qlxp:/home/root/mml> ./MMLCLI add -h
usage: MMLCLI [-h] [-n Resorce Name] [-g [Group Name]] [-N [Resorce Note]]

Add resource to MML

optional arguments:
  -h, --help            show this help message and exit
  -n Resorce Name, --name Resorce Name
  -g [Group Name], --group [Group Name]
  -N [Resorce Note], --note [Resorce Note]

* Example: 
    xgwang@linux-qlxp:/home/root/mml> ./MMLCLI add -n src5 -g group1
    [INFO ]: Successfully add resource[src5], id:10

```console


* update
```console
xgwang@linux-qlxp:/home/root/mml> ./MMLCLI update -h
usage: MMLCLI [-h] [-n Resorce Name] [-r [New Resource Name]]
              [-g [New Group Name]]

Update resource

optional arguments:
  -h, --help            show this help message and exit
  -n Resorce Name, --name Resorce Name
  -r [New Resource Name], --newname [New Resource Name]
  -g [New Group Name], --newgroup [New Group Name]

* Example:
xgwang@linux-qlxp:/home/root/mml> ./MMLCLI update -n src5 -r src5_new -g group2
[INFO ]: Successfully update resource
```console


* delete
```console
xgwang@linux-qlxp:/home/root/mml> ./MMLCLI delete -h
usage: MMLCLI [-h] [-n Resorce Name] [-s [Status]] [-g [Group Name]]

Update resource data

optional arguments:
  -h, --help            show this help message and exit
  -n Resorce Name, --name Resorce Name
  -s [Status], --status [Status]
  -g [Group Name], --group_name [Group Name]
                        Remove all resource within special group

* Example: 
xgwang@linux-qlxp:/home/root/mml> ./MMLCLI delete -n src5_new
Successfully delete resource [src5_new]
```console


* reserve
```console
xgwang@linux-qlxp:/home/root/mml> ./MMLCLI reserve -h
usage: MMLCLI [-h] [-n Resorce Name] [-d [Num S|M|H|D]]

Reserve resource data

optional arguments:
  -h, --help            show this help message and exit
  -n Resorce Name, --name Resorce Name
                        Reserve special resources thru source name
  -d [Num S|M|H|D], --duration [Num S|M|H|D]
* Example: 
xgwang@linux-qlxp:/home/root/mml> ./MMLCLI reserve -n src3 -d 4h
[INFO ]: Successfully update resource

```console

* release
```console
xgwang@linux-qlxp:/home/root/mml> ./MMLCLI release -h
usage: MMLCLI [-h] [-n Resorce Name]

Reserve resource data

optional arguments:
  -h, --help            show this help message and exit
  -n Resorce Name, --name Resorce Name
                        Release special resources thru source name

* Example:
xgwang@linux-qlxp:/home/root/mml> ./MMLCLI release -n src3
[INFO ]: Successfully update resource
```console
