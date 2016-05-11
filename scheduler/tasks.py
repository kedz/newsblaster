from __future__ import absolute_import
from celery import Task
from celery import group
from scheduler.celery import app
from scheduler.cluster import cluster_articles
from scheduler.summarize import summarize_clusters_lexrank
import sys
from sets import Set
import requests
import json
    
#TODO improve by checking the result of the request and rescheduling if an error was thrown
#TODO accept hostname and port as params

@app.task(ignore_result=True)
def schedule_all_spiders(job_dir):
	http_result = requests.get('http://localhost:6800/listspiders.json?project=default')
	result = json.loads(http_result.text)
	for spider in result['spiders']:
		_schedule_spider(spider,job_dir)

@app.task(ignore_result=True)
def schedule_newyork_times_spider(job_dir):
	_schedule_spider('newyork_times_rss',job_dir)

def _schedule_spider(spider_name,job_dir):
	payload = { 'project':'default' ,'spider':spider_name ,'setting':'JOBDIR='+ job_dir + '/' + spider_name }
	requests.post('http://localhost:6800/schedule.json',params=payload)


@app.task(ignore_result=True)
def do_clustering():
	cluster_articles()

@app.task(ignore_result=True)
def do_summarization():
	summarize_clusters_lexrank()
