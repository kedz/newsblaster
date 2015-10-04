from __future__ import absolute_import
from celery.schedules import crontab
from celery import Celery
import os
import yaml
from datetime import timedelta
from pprint import pprint

module_path = os.path.dirname(os.path.realpath(__file__))
config_dir = os.path.join(module_path,os.path.join('..' + os.sep + 'configs' ))
job_dir = os.path.join(module_path,os.path.join('..' + os.sep + 'nest' + os.sep + 'jobdir' ))
file_path = os.path.abspath(config_dir) + os.sep + 'settings.yaml'
config_file = open(file_path,'r')
config_data = yaml.load(config_file)

pprint(config_data)

BROKER_URL = "mongodb://%s:%d/jobs" %(config_data['mongodb']['hostname'],config_data['mongodb']['port'])

#Loads settings for Backend to store results of jobs
app = Celery('scheduler.celery',
		broker=BROKER_URL,
		backend=BROKER_URL,
		include=['scheduler.tasks']) 

#Schedule Config
app.conf.update(CELERYBEAT_SCHEDULE = {
                        'every-30-minutes-nyc_times': {
                        'task': 'scheduler.tasks.schedule_newyork_times_spider',
			                  'schedule': timedelta(minutes=30),
                        'args': (job_dir,)
                                        },
                        'every-hour-all-spiders': {
                        'task': 'scheduler.tasks.schedule_all_spiders',
			                  'schedule': timedelta(hours=3),
                        'args': (job_dir,)
                                        },
                    },
                    CELERY_TIMEZONE = 'US/Eastern',
                    CELERY_ACCEPT_CONTENT = ['pickle', 'json']
                    )

if __name__ == '__main__':
	app.start()
