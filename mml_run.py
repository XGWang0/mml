import atexit
import bottle

import db_opt
from job_timer import update_duration_task, jobtimer
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()

APP = bottle.Bottle()
APP_VERSION = '1.0'
'''
from threading import Timer
import datetime
def hello():
    print(datetime.datetime.now(), "hello, world")

t = Timer(2.0, hello)
t.start() 
'''

import time
def my_interval_job():
    while True:
        print(datetime.datetime.now(),'Hello World!')
        time.sleep(2)

def runtimer():
    jobtimer.MyTimer().run()

#sched.start()
# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: sched.shutdown(wait=False))

def resourceOpt():
    APP.route("/%s/ResourceSearch/<srcname>" %APP_VERSION, "GET", db_opt.ResourceOPT.searchResource)
    APP.route("/%s/ResourceNew" %APP_VERSION, "POST", db_opt.ResourceOPT.newResource)
    APP.route("/%s/ResourceUpdate" %APP_VERSION, "POST", db_opt.ResourceOPT.updateResource)
    APP.route("/%s/ResourceRelease" %APP_VERSION, "POST", db_opt.ResourceOPT.updateResource)
    APP.route("/%s/ResourceDelete/<srcname>" %APP_VERSION, "POST", db_opt.ResourceOPT.deleteResource)
    

resourceOpt()

import threading
#threading.Thread(target=APP.run, kwargs = {'host':'localhost', 'port':8080, 'debug':True, 'reloader':True}).start()
threading.Thread(target=jobtimer.MyTimer().run_scheduler, args=("update_dur", update_duration_task.UpDuration()(), 3)).start()
APP.run(host='localhost', port=8080, debug=True, reloader=True)