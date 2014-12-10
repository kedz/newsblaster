This module is uses [Celery](http://www.celeryproject.org/)  to  for scheduling the time or frequency when the Scrapy spiders run. Replaces Cron which is OS dependent and  poor in features required for software based projects.


Looking at the first step guide on [First Step With Celery Guide](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html) along with the associated docs should give you a good understanding of  what was done.

Currently Celery is scheduled to do the following:

 - Schedules New York Times spider every 30 minutes 
 - Schedules all implemented Spiders every 3 hours 

