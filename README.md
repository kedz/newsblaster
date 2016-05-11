
## NewsBlaster ##

Newsblaster is a system that helps users find the news that is of the most interest to them. The system automatically collects, clusters, categorizes, and summarizes news from several sites on the web (CNN, Reuters, Fox News, etc.) on a daily basis.

This is the group space being used to improve and further develop Columbia's NewsBlaster system.

----------
> NewsBlaster at Columbia University [Project](http://www.cs.columbia.edu/nlp/projects.cgi#newsblaster)

#### Installing ####

 1. Clone the repository 
     
    `git clone https://github.com/kedz/newsblaster.git`
 2. Go to the NewsBlaster directory 
 
      ` cd newsblaster/`
 
 3. Execute the install script 
     
      `./install.sh`
>This will install all dependencies and required files in your home directory by default. To override this please set `NB_HOME` . Example `export NB_HOME=/tmp/newsblaster`
  
#### Running ####
 4. Start NewsBlaster 
 
     `./newsblaster.sh start` 
     

 5. Check for news  articles . See Current Usage for details 

 >Crawls are currently configured to run on a 30 minutes to 3 hours schedule for some spiders. As a result you will not have articles until at least a minimum of 30 minutes.   This can be configured by changing the Celery schedule.  

 6. Stopping NewsBlaster 
 
   `./newsblaster stop`

#### Current Usage ####

>Documentation will be updated and changed as we continue to improve and build out NewsBlaster 

All summaries are currently stored in the MongoDB database automatically installed and configured when you deployed NewsBlaster.

Example a multi document summary can be seen below. 

```
> db.summaries.findOne()
{
	"_id" : ObjectId("573353f03168e60986fa1ac0"),
	"date" : ISODate("2016-05-11T11:46:56.488Z"),
	"summary_type" : "lexrank",
	"cluster_id" : ObjectId("573351a33168e60606eec00a"),
	"sentences" : [
		{
			"text" : "Brian Sandoval said Thursday he was \"incredibly grateful\" to be mentioned in the conversation over who President Obama would possibly select to replace Justice Antonin Scalia, but that he does \"not wish to be considered at this time\" for a spot on the U.S. Supreme Court.",
			"sentence_id" : 2,
			"article_id" : ObjectId("573347feb44be453490c5dde")
		},
		{
			"text" : "An intense political fight has erupted since the Feb. 13 death of long-serving conservative Justice Antonin Scalia, as Republicans maneuver to foil Obama's ability to choose a replacement who could tilt the court to the left for the first time in decades.",
			"sentence_id" : 2,
			"article_id" : ObjectId("57334808b44be453490c5e01")
		},
		{
			"text" : "The U.S. presidential election is set for Nov. 8 and Republicans want the next president to fill Scalia's vacancy, hoping a Republican will be elected.",
			"sentence_id" : 12,
			"article_id" : ObjectId("57334808b44be453490c5e01")
		},
		{
			"text" : "It's a duty that I take seriously, and one that I will fulfill in the weeks ahead,\" Obama, sounding undeterred by the Republican-led Senate's opposition, wrote in a blog post on the independent SCOTUSblog.com website.",
			"sentence_id" : 5,
			"article_id" : ObjectId("57334808b44be453490c5e01")
		},
		{
			"text" : "\"In the meantime, the American people are going to have the ability to gauge whether the person I've nominated is well within the mainstream, is a good jurist, is somebody who's worthy to sit on the Supreme Court,\" Obama told reporters in the Oval Office.",
			"sentence_id" : 30,
			"article_id" : ObjectId("573347feb44be453490c5dde")
		}
	]
}
```


API access to query summaries and related meta data will be exposed at a later date.



#### Papers ####

- Columbia Newsblaster: Multilingual News Summarization on the Web [Paper here ](http://www.aclweb.org/anthology/N04-3001)

- Columbia’s Newsblaster: New Features and Future Directions [Paper here (http://www.cs.columbia.edu/nlp/papers/2003/mckeown_al_03a.pdf)

- Tracking and Summarizing News on a Daily Basis with Columbia’s Newsblaster [Paper here ](http://www1.cs.columbia.edu/~sable/research/hlt-blaster.pdf)
