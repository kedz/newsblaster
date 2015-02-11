import elasticsearch
import json
from collections import defaultdict
from pprint import pprint
import sys

class NBQuery(object):

# TODO add authentication to ES
  def __init__(self,hostname='localhost.com',
                    port=9200,
                    user='user',
                    pw='password',
                    timeout=60):

    """Initializes and creates a connection to the ElasticSearch Cluster[ES]

    Function parameters are optional since the default localhost is used.

    Args:
      hostname(str): hostname of the ES cluster
      port(int): port of the ES cluster
    
    """
    self.es = elasticsearch.Elasticsearch(
        [hostname + ':' + str(port)], sniff_on_start=False, timeout=timeout)


  def _generate_match_sub_query(self,
                                content_query,
                                title_query,
                                source,
                                exact=True):
    
    query_body = defaultdict(dict)
    matches = []
    
    query_body["bool"]["must"] = matches

    if not exact:
      query_body["bool"]["should"] = matches


    if content_query is not None:
      content_dict = defaultdict(dict)
      content_dict["match"]["html_content"] = content_query 
      matches.append(content_dict)

    if title_query is not None:
      title_dict = defaultdict(dict)
      title_dict["match"]["title"] = title_query 
      matches.append(title_dict)

    if source is not None:
      source_filter = defaultdict(dict)
      source_filter["wildcard"]["source_link"] = source
      matches.append(source_filter) 


    # TODO complete date filter 
    # Must be completed for published_date in meta. Will have to review
    #date_filter = defaultdict(dict)
    #date_filter["range"]["time_of_crawl"] = {}
    #date_filter["range"]["time_of_crawl"]["from"] = "2015-02-02T10:00:00"
    #date_filter["range"]["time_of_crawl"]["to"] = "2015-01-30T02:18:50"
    #matches.append(date_filter) 
   
   #                                            "range" : {
   # "time_of_crawl" : {
   #     "gt" : "2015-01-01 00:00:00",
   #     "lt" : "2015-01-07 00:00:00"
   # }
   #},
    return query_body

  def _generate_metainfo_query(self,
                               topics,
                               author,  
                               language,
                               location,
                               start_date,
                               end_date):

    meta_query = defaultdict(dict)
   #"and": [
    #{"term": {"meta_information.topics": "snow"}},
    #{"term": {"meta_information.language": "en"}}
    #]

  def _generate_projections(self,projections):
    
    projections_gen = []
    if projections is None:
      projections_gen.append("title")
    else:
      projections_gen = projections_gen + projections

    return projections_gen
   

  def search(self,
            content_query=None,
            title_query=None,
            limit=None,
            topics=None,
            author=None,
            language=None,
            location=None,
            pub_start_date=None,
            pub_end_date=None,
            source=None,
            projections=None,
            timeout=60):

    """Used to search articles stored on ES

    Args:
      content_query(str): query term to be used to search html_content
      title_query(str) [optional]: query term to be used to search title
      limit(int) [optional]: max number of articles to returna
      topics(list of str) [optional]: topics that should be associated with the article
      author(list of str) [optional]: authors that should be associated with the article
      language(str) [optional]: language of the article
      location(str) [optional]: location of the article
      pub_start_date(str) [optional]: date when article was published in format 2015-01-07T00:00:00"
      pub_end_date(str) [optional]: date when article was published in format 2015-01-08T00:00:00" 
      source(str): the domain or source of the articles. Ex. nytimes.com
      projections(list of str): fields you will like to be returned. Ex. title, metainformation.topics
    
    """

    res_raw = self.es.search(index="news", timeout=timeout,body={
                                        "size": limit,
                                        "_source": self._generate_projections(projections),
                                            "query": {
                                              "filtered": {
                                                "query": self._generate_match_sub_query(content_query,title_query,source),
                                                "filter": {

                                                  "nested": {
                                                    "path": "meta_information",
                                                    "query":{
                                                      "filtered": {
                                                        "query": { "match_all": {}},
                                                        "filter": {
                                                          #"and": [
                                                            #{"term": {"meta_information.topics": "snow"}},
                                                            #{"term": {"meta_information.language": "en"}}
                                                          #]
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            },
                                        }
                  )
    
    sources = res_raw['hits']['hits'] 
    results = []
    
    for fields in sources:
      results.append(fields["_source"])
   
    return results 

  def update_document(self,document):
    pass

if __name__ == "__main__":
  pass
  #nb_query = NBQuery('island2.cs.columbia.edu')
  #["title","source_link","meta_information.topics","time_of_crawl" ,"meta_information.published_date"],
  #nb_query.search('snow storm',projections=["title","time_of_crawl"])
  #results = nb_query.search(source="www.nytimes.com*",projections=["title","source_link"],limit=100)
  #pprint(results)
