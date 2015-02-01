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
                    pw='password'):

    """Initializes and creates a connection to the ElasticSearch Cluster[ES]

    Function parameters are optional since the default localhost is used.

    Args:
      hostname(str): hostname of the ES cluster
      port(int): port of the ES cluster
    
    """
    self.es = elasticsearch.Elasticsearch([hostname + ':' + str(port)], sniff_on_start=True)


  def _generate_match_sub_query(self,
                                content_query,
                                title_query
                                exact=False):
    query_body = {}
    fields = []
    sub_query = 1
    #query_body["multi_match"] = {}
    #query_body["multi_match"]["type"] = "most_fields"
    #                                        {
    #                                      "multi_match" : {
    #                                      "query":      "sandy",
    #                                      "type":       "most_fields",
    #                                     "fields":     [ "title", "html_content" ]
    #                                      }},

    if content_query is not None:
      pass
      #content_query = "match:{" + "html_content:" +  content_query + "*}"  
      #content_dict = {"match":{ "html_content": content_query + "*" }}
      #pprint(list(content_dict))
      #d.setdefault("match",[]).append({ "html_content": content_query + "*" })
      #content_dict = dict()
      #content_dict['match'] = {'html_content': content_query + "*"}
      #content_dict['match']['html_content'] = content_query + "*"
      #sub_query.append(content_dict)

    if title_query is not None:
      pass
      #title_dict = {"match":{ "title": title_query + "*" }}
      #'match'['title'] = title_query + "*"  
      #title_query = "match:{" +  "title" +  title_query + "*}"  
      #d.setdefault("match",[]).append({ "title": title_query + "*" })
      #title_dict = defaultdict(dict)
      #title_dict['match']['title'] = content_query + "*"
      #sub_query.append(title_dict)

    print "********"
    #pprint(json.dumps(d))
    print "********"
                                   
    return sub_query
 
  def _generate_query(self,
                      content_query,
                      title_query=None,
                      limit=None,
                      topics=None,
                      author=None,
                      language=None,
                      location=None,
                      start_date=None,
                      end_date=None,
                      projections=None):


    #pprint(_generate_match_sub_query(content_query,title_query)


    #Automatically check title and html_content for match terms by default
    #TODO index should be a list read from config
    #TODO dynamically generate list here 


    #TODO split projections into array of strings
    #TODO convert dates
    #TODO split

    

    #res_raw = self.es.search(index="news", body={
    #                                    "size": 60,
    #                                    "_source": ["title","source_link"],
    #                                    "query":{ 
    #                                      "bool":{
    #                                      "should":[
    #                                        {"match": {"title": term + "*"}},
    #                                        {"match": {"html_content": term + "*"}}
    #                                              ]      
    #                                        }
    #                                      }
    #                                    }
    #              )

    pprint(self._generate_match_sub_query(content_query,title_query))
    #sys.exit(1) 
    #tt = { "html_content": content_query + "*" }

    res_raw = self.es.search(index="news", body={
                                        "size": 60,
                                        "_source": ["title","source_link","meta_information.topics"],
                                            "query": {
                                              "filtered": {
                                                "query": { "bool" : {
                "must" : [
                    {
                        "match" : {"title" : "snow"}
                    },
                    {
                        "match" : {"html_content" : "storm"}
                    }
                ]
            }
 },
                                                "filter": {
                                                  "nested": {
                                                    "path": "meta_information",
                                                    "query":{
                                                      "filtered": {
                                                        "query": { "match_all": {}},
                                                        "filter": {
                                                          "and": [
                                                            {"term": {"meta_information.topics": "snow"}},
                                                            {"term": {"meta_information.language": "en"}}
                                                          ]
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            },

                                         #"query":{"multi_match" : {
                                         # "query":      "snow storm",
                                         # "type":       "most_fields",
                                         #"fields":     [ "title", "html_content" ]
                                         # }},

                                        }
                  )

    sources = res_raw['hits']['hits'] 
    results = []
    
    for fields in sources:
      results.append(fields["_source"])
   
    pprint(results)

  def search(self,query):
    """Searches ES for articles/documents based on users terms

    Args:
    
    Returns:

    *Consider template query in future 
    """
    self._generate_query(query,query)
    #es.search(index="my_app", body={"query": {"match": {"title": "elasticsearch"}}})

  def save_files(self,path):
    pass
  
  def get_html_source(self,query,path):
    pass

  def update_document(self,document):
    pass

if __name__ == "__main__":
  nb_query = NBQuery('island2.cs.columbia.edu')
  nb_query.search('snow storm')
