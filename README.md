
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

You are currently able to query and retrieve articles based on a variety of  meta information. Please see our [iPython Notebook](http://nbviewer.ipython.org/github/kedz/newsblaster/blob/master/notebooks/query_articles.ipynb) 

 All article have the following attributes associated with them.

![JSON structure of each article ](https://github.com/kedz/newsblaster/blob/master/documentation/article_json.png)


#### Papers ####

- Columbia Newsblaster: Multilingual News Summarization on the Web [Paper here ](http://www.aclweb.org/anthology/N04-3001)

- Columbia’s Newsblaster: New Features and Future Directions [Paper here (http://www.cs.columbia.edu/nlp/papers/2003/mckeown_al_03a.pdf)

- Tracking and Summarizing News on a Daily Basis with Columbia’s Newsblaster [Paper here ](http://www1.cs.columbia.edu/~sable/research/hlt-blaster.pdf)
